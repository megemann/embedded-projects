# nec_send_generic.py
# Minimal NEC sender module (import and call send_cmd).
# Requires pigpio daemon: sudo pigpiod

import pigpio, time

# Defaults
CARRIER_HZ = 38000
ADDR_DEFAULT = 0x00

# NEC timings (microseconds)
LEAD_M = 9000
LEAD_S = 4500
MARK   = 560
SPACE0 = 560
SPACE1 = 1690
REPT_S = 2250

def _bits_lsb(b: int):
    return [(b >> i) & 1 for i in range(8)]

def _nec_bits(addr: int, cmd: int):
    return (_bits_lsb(addr) +
            _bits_lsb(addr ^ 0xFF) +
            _bits_lsb(cmd)  +
            _bits_lsb(cmd ^ 0xFF))

def _build_full_wave(pi: pigpio.pi, gpio: int, bits, carrier: int):
    half = int(1_000_000 / carrier / 2)
    wf = []

    def mark(us):
        cycles = int(carrier * us / 1_000_000.0)
        for _ in range(cycles):
            wf.append(pigpio.pulse(1 << gpio, 0, half))
            wf.append(pigpio.pulse(0, 1 << gpio, half))

    def space(us):
        if us > 0:
            wf.append(pigpio.pulse(0, 0, us))

    # Leader
    mark(LEAD_M); space(LEAD_S)
    # 32 data bits
    for b in bits:
        mark(MARK)
        space(SPACE0 if b == 0 else SPACE1)
    # Trailer
    mark(MARK)

    pi.wave_clear()
    pi.wave_add_generic(wf)
    wid = pi.wave_create()
    if wid < 0:
        raise RuntimeError(f"wave_create failed: {wid}")
    return wid

def _build_repeat_wave(pi: pigpio.pi, gpio: int, carrier: int):
    half = int(1_000_000 / carrier / 2)
    wf = []

    def mark(us):
        cycles = int(carrier * us / 1_000_000.0)
        for _ in range(cycles):
            wf.append(pigpio.pulse(1 << gpio, 0, half))
            wf.append(pigpio.pulse(0, 1 << gpio, half))

    def space(us):
        if us > 0:
            wf.append(pigpio.pulse(0, 0, us))

    mark(LEAD_M); space(REPT_S); mark(MARK)

    pi.wave_clear()
    pi.wave_add_generic(wf)
    wid = pi.wave_create()
    if wid < 0:
        raise RuntimeError(f"wave_create (repeat) failed: {wid}")
    return wid

def send_cmd(cmd: int,
             gpio: int = 18,
             addr: int = ADDR_DEFAULT,
             repeats: int = 0,
             gap_ms: int = 110,
             carrier: int = CARRIER_HZ,
             pi: pigpio.pi | None = None) -> None:
    """
    Send a single NEC command (with optional repeats).
      cmd: command byte (0x00..0xFF)
      gpio: Pi GPIO driving the TX module DAT/IN
      addr: NEC address byte (default 0x00)
      repeats: number of NEC repeat frames after the full frame
      gap_ms: gap between frames for repeats
      carrier: carrier frequency in Hz (default 38 kHz)
      pi: optional existing pigpio.pi() instance to reuse
    """
    own_pi = False
    if pi is None:
        pi = pigpio.pi()
        if not pi.connected:
            raise SystemExit("pigpio not running. Start with: sudo pigpiod")
        own_pi = True

    try:
        pi.set_mode(gpio, pigpio.OUTPUT)
        bits = _nec_bits(addr, cmd)

        wid = _build_full_wave(pi, gpio, bits, carrier)
        pi.wave_send_once(wid)
        while pi.wave_tx_busy():
            time.sleep(0.001)
        pi.wave_delete(wid)

        if repeats > 0:
            wid_rep = _build_repeat_wave(pi, gpio, carrier)
            for _ in range(repeats):
                time.sleep(gap_ms / 1000.0)
                pi.wave_send_once(wid_rep)
                while pi.wave_tx_busy():
                    time.sleep(0.001)
            pi.wave_delete(wid_rep)
    finally:
        if own_pi:
            pi.stop()

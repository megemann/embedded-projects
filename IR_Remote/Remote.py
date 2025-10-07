from Send_CMD import send_cmd

class Remote:
    def __init__(self, gpio, instructions, start_state):
        self.gpio = gpio
        self.instructions = instructions # dict ("Command": cmd)
        self.current_state = start_state

    def change_state(self, new_state):

        """
        if current_state == new_state:
            return current_state
        else:
            if (current_state[1] == new_state[1]):
                led_overlap = overlapping_cmds.get(new_state[0])
                picture_overlap = overlapping_cmds.get(new_state[1])
                if led_overlap and picture_overlap:
                    if current_state[1] == led_overlap: # same command
                        send_cmd(rgb_cmds[new_state[0]], self.gpio) # will be fine, wont change
                    else:
                        raise Exception("Overlapping commands are not allowed")
                elif led_overlap:
                    send_cmd(rgb_cmds[new_state[0]], self.gpio) # change to (new_state, altered_state)
                    send_cmd(picture_cmds[new_state[1]], self.gpio) # change to (new_state, old_state)
                else:
                    send_cmd(rgb_cmds[new_state[0]], self.gpio) # change to (new_state, old_state)
            else:
                led_overlap = overlapping_cmds.get(new_state[0])
                picture_overlap = overlapping_cmds.get(new_state[1])
                if led_overlap and picture_overlap:
                    if current_state[0] == picture_overlap: # same command
                        send_cmd(rgb_cmds[new_state[0]], self.gpio) # will be fine, wont change
                    else:
                        raise Exception("Overlapping commands are not allowed")
                elif picture_overlap: # we change picture with led command
                    send_cmd(picture_cmds[new_state[1]], self.gpio) # change to (altered_state, new_state)
                    send_cmd(rgb_cmds[new_state[0]], self.gpio) # change to (old_state, new_state)
                else:
                    send_cmd(picture_cmds[new_state[1]], self.gpio) # change to (old_state, new_state)

            return new_state
        """

        print(self.gpio, "to", new_state)
        if self.current_state == new_state:
            return self.current_state
        else:
            send_cmd(self.instructions[new_state], self.gpio)
            return new_state

rgb_cmds = {
    "power": 0x40,
    "white": 0x44,
    "blue": 0x45,
    "green": 0x59,
    "red": 0x58,
    "bright up": 0x5C,
    "bright down": 0x5D,
    "play": 0x41,
    "orange": 0x54,
    "light green": 0x55,
    "mid-blue": 0x49,
    "red-orange": 0x50,
    "blue-green": 0x51,
    "blue-purple": 0x4D,
    "green-yellow": 0x1C,
    "aquamarine": 0x1D,
    "light-purple": 0x1E,
    "yellow": 0x18,
    "green-blue": 0x19,
    "purple": 0x1A,
    "music1": 0x48,
    "music2": 0x4C,
    "music3": 0x1F,
    "music4": 0x1B,
    "more-red": 0x14,
    "less-red": 0x10,
    "more-green": 0x15,
    "less-green": 0x11,
    "more-blue": 0x16,
    "less-blue": 0x12,
    "fade": 0x07,
    "slow": 0x13,
    "quick": 0x0F,
}

rgb_turn_on_cmds = {
    "power": 0x40,
}

picture_cmds = {
    "on": 0x45,
    "off": 0x47,
    "static": 0x44,
    "auto_day": 0x40,
    "auto_night": 0x43,
    "white-light": 0x07,
    "warm": 0x15,
    "neutral": 0x09,
    "darker": 0x16,
    "brighter": 0x0D,
    "5-min": 0x0C,
    "15-min": 0x18,
    "30-min": 0x5E,
}

picture_turn_on_cmds = {
    "on": 0x45,
    "auto_day": 0x40,
    "auto_night": 0x43,
    "static": 0x44,
    "5-min": 0x0C,
    "15-min": 0x18,
    "30-min": 0x5E,
}


overlapping_cmds = {
    "white": "static",
    "static": "white",
    "blue": "on",
    "on": "blue",
    "white-light": "fade",
    "fade": "white-light",
    "power": "auto_day",
    "auto_day": "power",
    "more-green": "warm",
    "warm": "more-green",
    "more-blue": "darker",
    "darker": "more-blue",
    "yellow": "15-min",
    "15-min": "yellow",
}



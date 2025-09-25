from LED_IR_Control.Send_CMD import send_cmd


def change_state(current_state, new_state):
    if current_state == new_state:
        return current_state
    else:
        if (new_state not in overlapping_cmds):
            if (current_state in overlapping_cmds):
                if (overlapping_cmds[0] == current_state):
                    send_cmd(rgb_cmds[new_state])
                else:
                    send_cmd(picture_cmds[new_state])
            else:

    # TODO: Think of all possible overlapping cases and states


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
    "white": ("white", "static"),
    "static": ("white", "static"),
    "blue": ("blue", "on"),
    "on": ("blue", "on"),
    "white-light": ("white-light", "fade"),
    "fade": ("white-light", "fade"),
    "power": ("power", "auto_day"),
    "auto_day": ("power", "auto_day"),
    "more-green": ("more-green", "warm"),
    "warm": ("more-green", "warm"),
    "more-blue": ("more-blue", "darker"),
    "darker": ("more-blue", "darker"),
    "yellow": ("yellow", "15-min"),
    "15-min": ("yellow", "15-min"),
}






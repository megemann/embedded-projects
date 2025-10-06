from LED_IR_Control.Send_CMD import send_cmd

def run_remote():
    # power simply denotes the last button pressed -> right now we dont have any state tracking
    current_state = ("white", "off") # (led, picture)
    
    print("=== LED Remote Control ===")
    print(f"Current state: LED={current_state[0]}, Picture={current_state[1]}")
    
    while True:
        print("\n" + "="*50)
        print("Select LED color:")
        led_options = list(rgb_cmds.keys())
        for i, option in enumerate(led_options, 1):
            print(f"{i:2d}. {option}")
        
        try:
            led_choice = int(input(f"\nEnter LED choice (1-{len(led_options)}): ")) - 1
            if 0 <= led_choice < len(led_options):
                led_state = led_options[led_choice]
                print(f"\nSelected LED: {led_state}")
            else:
                print("Invalid choice!")
                continue
        except ValueError:
            print("Please enter a number!")
            continue
        
        print("\nSelect Picture mode:")
        picture_options = list(picture_cmds.keys())
        for i, option in enumerate(picture_options, 1):
            print(f"{i:2d}. {option}")
        
        try:
            picture_choice = int(input(f"\nEnter Picture choice (1-{len(picture_options)}): ")) - 1
            if 0 <= picture_choice < len(picture_options):
                picture_state = picture_options[picture_choice]
                print(f"Selected Picture: {picture_state}")
            else:
                print("Invalid choice!")
                continue
        except ValueError:
            print("Please enter a number!")
            continue
        
        # Update states
        new_state = (led_state, picture_state)
        print(f"\nChanging to: LED={led_state}, Picture={picture_state}")
        
        try:
            current_state = change_state(current_state, new_state)
            print("✓ State changed successfully!")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        print(f"Current state: LED={current_state[0]}, Picture={current_state[1]}")
        
        # Ask if they want to continue
        continue_choice = input("\nContinue? (y/n): ").lower()
        if continue_choice not in ['y', 'yes', '']:
            break
    
    print("\nGoodbye!")
    

def change_state(current_state, new_state):
    if current_state == new_state:
        return current_state
    else:
        if (current_state[1] == new_state[1]):
            led_overlap = overlapping_cmds.get(new_state[0])
            picture_overlap = overlapping_cmds.get(new_state[1])
            if led_overlap and picture_overlap:
                if current_state[1] == led_overlap: # same command
                    send_cmd(rgb_cmds[new_state[0]]) # will be fine, wont change
                else:
                    raise Exception("Overlapping commands are not allowed")
            elif led_overlap:
                send_cmd(rgb_cmds[new_state[0]]) # change to (new_state, altered_state)
                send_cmd(picture_cmds[new_state[1]]) # change to (new_state, old_state)
            else:
                send_cmd(rgb_cmds[new_state[0]]) # change to (new_state, old_state)
        else:
            led_overlap = overlapping_cmds.get(new_state[0])
            picture_overlap = overlapping_cmds.get(new_state[1])
            if led_overlap and picture_overlap:
                if current_state[0] == picture_overlap: # same command
                    send_cmd(rgb_cmds[new_state[0]]) # will be fine, wont change
                else:
                    raise Exception("Overlapping commands are not allowed")
            elif picture_overlap: # we change picture with led command
                send_cmd(picture_cmds[new_state[1]]) # change to (altered_state, new_state)
                send_cmd(rgb_cmds[new_state[0]]) # change to (old_state, new_state)
            else:
                send_cmd(picture_cmds[new_state[1]]) # change to (old_state, new_state)
            


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

if __name__ == "__main__":
    run_remote()




import pygame

class JoystickHandler:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joysticks = {}

        # Buttons dictionary (fixed key list)
        self.button_states = {key: False for key in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l","up", "down", "left", "right"]}

        # Dictionary to store axis values separately
        self.axis_states = {key:0.00 for key in range(6)}

        # Button mappings (mapping button index to dictionary keys)
        self.button_actions = {
            0: "a",  # Button green -> "a"
            1: "b",  # Button red -> "b"
            2: "c",  # Button blue -> "c"
            3: "d",  # Button yellow -> "d"
            4: "e",  # Left Bumper -> "e"
            5: "f",  # Right Bumper -> "f"
            6: "g",  # Left Stick -> "g"
            7: "h",  # Right Stick -> "h"
            8: "i",  # Right Button -> "i"
            9: "j",  # Left Button -> "j"
            10: "k",
            11: "l",
            (0,1): "up",
            (0,-1): "down",
            (1,0): "right",
            (-1,0): "left"
        }

    def add_joy(self, joy_id):
        if joy_id not in self.joysticks:
            joystick = pygame.joystick.Joystick(joy_id)
            joystick.init()
            self.joysticks[joy_id] = joystick
            print(f"✅ Joystick with ID {joy_id} is connected.")

    def remove_joy(self, joy_id):
        if joy_id in self.joysticks:
            print(f"❌ Joystick {self.joysticks[joy_id].get_name()} (ID: {joy_id}) disconnected.")
            self.joysticks[joy_id].quit()
            del self.joysticks[joy_id]
            print("⚠️ Please reconnect your joystick!")
        # elif joy_id not in self.joysticks:
        #     joystick = pygame.joystick.Joystick(joy_id)
        #     joystick.init()
        #     self.joysticks[joy_id] = joystick  # Store joystick object instead of True
        #     print(f"✅ Joystick {joystick.get_name()} (ID: {joy_id}) connected.")

    def handle_joy(self):
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.JOYDEVICEADDED:
                self.add_joy(event.device_index)
            elif event.type == pygame.JOYDEVICEREMOVED:
                self.remove_joy(event.instance_id)
            elif event.type == pygame.JOYAXISMOTION:
                # Store axis values in the axis_states dictionary
                self.axis_states[event.axis] = round(event.value, 2)
                self.print_results(f"Axis {event.axis} moved")
            elif event.type == pygame.JOYHATMOTION:
                directions = self.button_actions.get(event.value, "neutral")
                if directions != "neutral":
                    self.button_states[directions] = not self.button_states.get(directions, False)
                    state_text = "pressed" if self.button_states[directions] else "released"
                    self.print_results(f"{directions} {state_text}")
            
            elif event.type == pygame.JOYBUTTONDOWN:
                button_name = self.button_actions.get(event.button, None)
                if button_name and button_name in self.button_states:
                    # Toggle the button state
                    self.button_states[button_name] = not self.button_states[button_name]
                    state_text = "pressed" if self.button_states[button_name] else "released"
                    self.print_results(f"{button_name} {state_text}")

        return True
    
    def print_results(self, message = None):
        merged_dict = {**self.button_states, **self.axis_states}
        # print(f"{message} → {merged_dict}")
        return merged_dict

# Initialize and start loop
# JOYSTICK_HANDLER = JoystickHandler()
# run = True
# while run:
#     run = JOYSTICK_HANDLER.handle_joy()

# pygame.quit()
# print("Exiting program.")

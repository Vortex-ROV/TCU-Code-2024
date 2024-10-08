import unittest
import pygame
from communication.message import Message
import copy
import json
import pygame
from PyQt5.QtCore import QThread, pyqtSignal
import time

# from auto_transplanting import AutoTransplanting


class JoyStick(QThread):
    signal = pyqtSignal(bytes)

    def __init__(self):
        super().__init__()

        pygame.init()
        pygame.joystick.init()

        self.__joystick = None
        self.__joystick_name = None
        self.__configs = {}

        self.__message = Message()
        self.__old_message = Message()

        self.__prev_state = []
        self.__prev_input = []

        self.__arm_rotating_gripper = False

        # self.auto_transplanting = AutoTransplanting(1)

    def __get_button_state(self, butt_num, toggle=True):
        if not toggle:
            return self.__joystick.get_button(butt_num)

        input = self.__joystick.get_button(butt_num)
        if input and not self.__prev_input[butt_num]:
            self.__prev_state[butt_num] = not self.__prev_state[butt_num]

        self.__prev_input[butt_num] = input
        return self.__prev_state[butt_num]

    def __map_axis(self, axis_value) -> int:
        base = 1500
        range = 160
        tolerance = 0.05

        if axis_value > tolerance or axis_value < -tolerance:
            return int(axis_value * range + base)
        else:
            return 1500

    def __handle_input(self):
        self.__message.set_value(
            "throttle",
            self.__map_axis(self.__joystick.get_axis(self.__configs["throttle"])),
        )
        self.__message.set_value(
            "yaw",
            self.__map_axis(
                (self.__joystick.get_axis(self.__configs["yaw_r"]) / 2 + 0.5)
                - (self.__joystick.get_axis(self.__configs["yaw_l"]) / 2 + 0.5)
            ),
        )
        self.__message.set_value(
            "forward",
            self.__map_axis(-self.__joystick.get_axis(self.__configs["forward"])),
        )
        self.__message.set_value(
            "lateral",
            self.__map_axis(self.__joystick.get_axis(self.__configs["lateral"])),
        )

        self.__message.set_value(
            "gripper_1", self.__get_button_state(self.__configs["gripper_1"])
        )
        self.__message.set_value(
            "gripper_2", self.__get_button_state(self.__configs["gripper_2"])
        )

        if self.__get_button_state(self.__configs["light"]):
            self.__message.set_value("light", "H")
        else:
            self.__message.set_value("light", "0")

        self.__arm_rotating_gripper = self.__get_button_state(
            self.__configs["arm_rotating_gripper"]
        )

        if (
            self.__arm_rotating_gripper
            and self.__get_button_state(
                self.__configs["rotating_gripper_left"], toggle=False
            )
            and not self.__get_button_state(
                self.__configs["rotating_gripper_right"], toggle=False
            )
        ):
            self.__message.set_value("rotating_gripper", "L")
        elif (
            self.__arm_rotating_gripper
            and self.__get_button_state(
                self.__configs["rotating_gripper_right"], toggle=False
            )
            and not self.__get_button_state(
                self.__configs["rotating_gripper_left"], toggle=False
            )
        ):
            self.__message.set_value("rotating_gripper", "R")
        else:
            self.__message.set_value("rotating_gripper", "O")

        if not self.__message.get_value("armed") and self.__get_button_state(
            self.__configs["arm"], toggle=False
        ):
            self.__message.set_value("armed", True)
        if self.__message.get_value("armed") and self.__get_button_state(
            self.__configs["disarm"], toggle=False
        ):
            self.__message.set_value("armed", False)

        # set flight modes
        if (
            self.__joystick_name == "Xbox 360 Controller"
            or self.__joystick_name == "Controller (Xbox One For Windows)"
        ):
            if self.__joystick.get_hat(0)[0] == 1:
                self.__message.set_value("flight_mode", "S")
            elif self.__joystick.get_hat(0)[0] == -1:
                self.__message.set_value("flight_mode", "A")
            elif self.__joystick.get_hat(0)[1] == 1:
                self.__message.set_value("flight_mode", "M")
        elif (
            self.__joystick_name == "DualSense Wireless Controller"
            or self.__joystick_name == "PS4 Controller"
        ):
            if self.__joystick.get_button(11):
                self.__message.set_value("flight_mode", "S")
            elif self.__joystick.get_button(12):
                self.__message.set_value("flight_mode", "A")
            elif self.__joystick.get_button(13):
                self.__message.set_value("flight_mode", "M")

        # set flight mode to depth hold and stop motor control when rotating gripper is armed
        if self.__arm_rotating_gripper:
            self.__message.set_value("flight_mode", "A")
            self.__message.set_value("throttle", 1500)
            self.__message.set_value("yaw", 1500)
            self.__message.set_value("forward", 1500)
            self.__message.set_value("lateral", 1500)

        self.send_values()

        # auto transplanting :(
        """
        self.auto_transplanting.do_plan(self.__new_values, self.signal)
        if self.auto_transplanting.autonomus_plan == 1:
            if self.auto_transplanting.autonomus != 2:
                self.send_values()
        elif self.auto_transplanting.autonomus_plan == 2:
            if self.auto_transplanting.autonomus == 0:
                self.send_values()

        if self.__get_button_state(self.__configs["auto"]):
            self.auto_transplanting.increament()

        self.__updated_old_button_input_list([self.__configs["auto"]])

        if self.__get_button_state(6):
            print("saved pressure at prop")
            self.auto_transplanting.pressure_at_prop = 100

        if self.__get_button_state(7):
            print("saved pressure above prop")
            self.auto_transplanting.pressure_above_prop = 200
        """

    # more auto transplanting :(
    """
    def get_pressure(self, data):

        if len(self.__old__button_input) and self.__joystick is not None:
            if self.__get_button_state(6):
                print("saved pressure at prop")
                self.auto_transplanting.pressure_at_prop = float(data[36:42])

            if self.__get_button_state(7):
                print("saved pressure above prop")
                self.auto_transplanting.pressure_above_prop = float(data[36:42])

            self.auto_transplanting.current_pressure = float(data[36:42])
            self.__updated_old_button_input_list([6, 7])
    """

    def send_values(self):
        if self.__old_message == self.__message:
            return

        self.__old_message = copy.deepcopy(self.__message)
        print(len(self.__message.bytes()))
        self.signal.emit(self.__message.bytes())
        time.sleep(0.01)

    def __handle_joystick_disconnect(self):
        if pygame.joystick.get_count() > 0 and self.__joystick is not None:
            return

        while pygame.joystick.get_count() == 0:
            self.__message = Message()
            if self.__message != self.__old_message:
                self.__old_message = copy.deepcopy(self.__message)
                self.signal.emit(self.__message.bytes())

            print("No joystick connected")
            pygame.time.wait(100)

        self.__message.set_value("joystick_connect", True)
        self.__old_message = copy.deepcopy(self.__message)
        self.signal.emit(self.__message.bytes())

        print("joystick connected succesfully")
        self.__joystick = pygame.joystick.Joystick(0)
        self.__joystick.init()

        self.__joystick_name = self.__joystick.get_name()
        print("Joystick Name:", self.__joystick_name)

        self.__load_joystick_configurations("Src/joystick/configurations.json")
        self.__prev_state = [False for _ in range(self.__configs["buttons_cnt"])]
        self.__prev_input = [False for _ in range(self.__configs["buttons_cnt"])]

    def connect_signal(self, slot):
        self.signal.connect(slot)

    def __load_joystick_configurations(self, json_path):
        data = {}
        try:
            with open(json_path) as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")

        self.__configs = data[self.__joystick_name]

    def run(self):
        clock = pygame.time.Clock()
        fps = 60

        while True:
            self.__handle_joystick_disconnect()
            pygame.event.pump()
            self.__handle_input()
            clock.tick(fps)


class Test(unittest.TestCase):

    def test(self):
        joystick = JoyStick()
        joystick.run()


if __name__ == "__main__":
    unittest.main()

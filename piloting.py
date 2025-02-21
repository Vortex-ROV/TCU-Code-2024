from pymavlink import mavutil 
import serial
import sys
import time
from communication.socket.client import ClientSocket
import json
from joystick.JoystickHandler import JoystickHandler

positive_pwm = 1800
negative_pwm = 1200
zero_pwm = 1500
gripper_1 = 0 #pin
gripper_2 = 0 #pin
gripper_3 = 0 #pin
gripper_on = 5000
gripper_off = 0
THROTTLE_RC_CHANNEL = 3
YAW_RC_CHANNEL = 4
FORWARD_RC_CHANNEL = 5
LATERAL_RC_CHANNEL = 6


class ROVController:
    def __init__(self):
        # self.master = mavutil.mavlink_connection("udp:" + "192.168.33.100" + ":" + str(14550), 115200)
        # self.master = mavutil.mavlink_connection("udp:" + "172.23.160.1" + ":" + str(14550), 115200)
        # self.master = mavutil.mavlink_connection("COM6", 115200)
        # self.master.wait_heartbeat()
        print("heartbeat detected")
        self.client = ClientSocket("192.168.33.1", 4096)
        self.client.connect()
        self.old_message = ""
        self.yaw = 0
        self.rc_channel_values = [1500, 1500, 1500, 1500, 1500, 1500, 65535, 65535]
        self.tools_dict = {
            "led": False,
            "pump1": False,
            "pump2": False,
            "servo": 0,
            "gripper_1": False,
            "gripper_2": False,
            "gripper_3": False,
        }

        self.channels = {
            0: self.lateral_channel,
            1: self.forward_channel,
            3: self.throttle_channel, 
            4: self.yaw_channel_left,
            5: self.yaw_channel_right,
            "a": self.led,
            "b": self.pump1,
            "c": self.pump2,
            "d": self.servo,
            "e": self.gripper_1,
            "f": self.gripper_2,
            "g": self.gripper_3,
            "h": self.arm_disarm,
            "up": self.set_stabilize,
            "down": self.set_alt_hold,
            "right": self.set_manual,
        }

    def map_value(self , value, from_low, from_high, to_low, to_high):
        # Map the value from one range to another
        return to_low + (float(value - from_low) / float(from_high - from_low) * (to_high - to_low))

    def set_rc_channels_pwm(self):
        self.rc_channel_values = [int(x) for x in self.rc_channel_values]
        print("rc channels:", self.rc_channel_values)
        # self.master.mav.rc_channels_override_send(
        #     self.master.target_system,
        #     self.master.target_component,
        #     *self.rc_channel_values
        # )

    def set_servo_pwm(self, servo, pwm):
        # self.master.mav.command_long_send(
        #     self.master.target_system,
        #     self.master.target_component,
        #     mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        #     0,
        #     servo,
        #     pwm,
        #     0, 0, 0, 0, 0
        # )
        print("set_servo_pwm", servo, pwm)

    def yaw_channel_left(self, pwm):
        pwm = (pwm + 1) / 2
        self.yaw -= pwm

    def yaw_channel_right(self, pwm):
        pwm = (pwm + 1) / 2
        self.yaw += pwm

    def yaw_channel(self, pwm):
        pwm = self.map_value(pwm, -1, 1, negative_pwm, positive_pwm)
        self.rc_channel_values[YAW_RC_CHANNEL - 1] = pwm
        # print("yaw_channel", pwm)
        self.yaw = 0

    def lateral_channel(self, pwm):
        pwm = self.map_value(pwm, -1, 1, negative_pwm, positive_pwm)
        # print("lateral_channel", pwm)
        self.rc_channel_values[LATERAL_RC_CHANNEL - 1] = pwm

    def throttle_channel(self, pwm):
        pwm = self.map_value(pwm, -1, 1, negative_pwm, positive_pwm)
        # print("throttle_channel", pwm)
        self.rc_channel_values[THROTTLE_RC_CHANNEL - 1] = pwm

    def forward_channel(self, pwm):
        pwm = self.map_value(pwm, -1, 1, negative_pwm, positive_pwm)
        # print("forward_channel", pwm)
        self.rc_channel_values[FORWARD_RC_CHANNEL - 1] = pwm

    def gripper_1(self, on):
        print("gripper_1_channel", on)
        self.tools_dict["gripper_1"] = on

    def gripper_2(self, on):
        print("gripper_2_channel", on)
        self.tools_dict["gripper_2"] = on

    def gripper_3(self, on):
        print("gripper_3_channel", on)
        self.tools_dict["gripper_3"] = on

    def led(self, on):
        print("led", on)
        self.tools_dict["led"] = on

    def pump1(self, on):
        print("pump1", on)
        self.tools_dict["pump1"] = on

    def pump2(self, on):
        print("pump2", on)
        self.tools_dict["pump2"] = on

    def servo(self, pwm):
        print("servo", pwm)
        self.tools_dict["servo"] = int(pwm * 255.0)

    def arm_disarm(self, on):
        print("arm_disarm", on)
        # if on:
        #     self.master.arducopter_arm()
        # else:
        #     self.master.arducopter_disarm()
            
    def set_alt_hold(self, on):
        print("set_alt_hold", on)
        if not on:
            return
        
        # mode = "ALT_HOLD"
        # if mode not in self.master.mode_mapping():
        #     print('Unknown mode : {}'.format(mode))
        #     print('Try:', list(self.master.mode_mapping().keys()))
        #     sys.exit(1)

        # mode_id = self.master.mode_mapping()[mode]
        # self.master.mav.set_mode_send(
        #     self.master.target_system,
        #     mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        #     mode_id
        # )

    def set_manual(self, on):
        print("set_manual", on)
        if not on:
            return
        
        # mode = "MANUAL"
        # if mode not in self.master.mode_mapping():
        #     print('Unknown mode : {}'.format(mode))
        #     print('Try:', list(self.master.mode_mapping().keys()))
        #     sys.exit(1)

        # mode_id = self.master.mode_mapping()[mode]
        # self.master.mav.set_mode_send(
        #     self.master.target_system,
        #     mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        #     mode_id
        # )

    def set_stabilize(self, on):
        print("set_stabilize", on)
        if not on:
            return
        
        # mode = "STABILIZE"
        # if mode not in self.master.mode_mapping():
        #     print('Unknown mode : {}'.format(mode))
        #     print('Try:', list(self.master.mode_mapping().keys()))
        #     sys.exit(1)

        # mode_id = self.master.mode_mapping()[mode]
        # self.master.mav.set_mode_send(
        #     self.master.target_system,
        #     mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        #     mode_id
        # )

    def process_message(self, msg):
        for key in self.channels:
            if key in msg:
                self.channels[key](msg[key])

        self.yaw_channel(self.yaw)
        self.set_rc_channels_pwm()

        serialized_dict = json.dumps(self.tools_dict)
        print(serialized_dict)
        
        if serialized_dict != self.old_message:
            self.old_message = serialized_dict
            self.client.send(serialized_dict.encode('utf-8'))
        

if __name__ == "__main__":
    rov_controller = ROVController()
    joystick = JoystickHandler()
    while True:
        joystick.handle_joy()
        msg = joystick.print_results()
        # print(msg)
        rov_controller.process_message(msg)



from pymavlink import mavutil 
import serial
import socket
import sys
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


class ROVController:
    def __init__(self):
        # self.master = mavutil.mavlink_connection("udp:" + "192.168.33.100" + ":" + str(14550), 115200)
        # self.master.wait_heartbeat()
        # self.client = ClientSocket("192.168.33.1", 4096)
        # self.client.connect()
        self.old_message = ""
        self.yaw = 0
        self.tools_dict = {
            
            "gripper_1": False,
            "gripper_2": False,
            "gripper_3": False
        }

        self.channels = {
            3: self.throttle_channel, 
            4: self.yaw_channel_left,
            0: self.lateral_channel,
            1: self.forward_channel,
            5: self.yaw_channel_right,
            "e": self.gripper_1_channel,
            "f": self.gripper_2_channel,
            "g": self.gripper_3_channel,
            "H": self.arm_disarm,
            "up": self.set_stabilize,
            "down": self.set_alt_hold,
            "right": self.set_manual,
        }
    def map_value(self , value, from_low, from_high, to_low, to_high):
    # Map the value from one range to another
        return to_low + (float(value - from_low) / float(from_high - from_low) * (to_high - to_low))

    def set_rc_pwm(self, channel, pwm):
        # self.master.mav.rc_channels_override_send(
        #     self.master.target_system,
        #     self.master.target_component,
        #     pwm,
        #     channel
        # )
        # print("set_rc_pwm", channel, pwm)
        pass

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
        # print("set_servo_pwm", servo, pwm)
        pass

    def yaw_channel_left(self, pwm):
        pwm = (pwm + 1) / 2
        self.yaw -= pwm

    def yaw_channel_right(self, pwm):
        pwm = (pwm + 1) / 2
        self.yaw += pwm

    def yaw_channel(self, pwm):
        pwm = self.map_value(pwm, -1, 1, negative_pwm, positive_pwm)
        self.set_rc_pwm(1, pwm)
        print("yaw_channel", pwm)
        self.yaw = 0


    def lateral_channel(self, pwm):
        self.set_rc_pwm(2, pwm)
        # print("lateral_channel", pwm)

    def gripper_1_channel(self, on):
        if on:
            self.tools_dict["gripper_1"] = True
            # print("gripper_1_channel", on)
        else:   
            self.tools_dict["gripper_1"] = False
            # print("gripper_1_channel", on)

    def gripper_2_channel(self, on):
        if on:
            self.tools_dict["gripper_2"] = True
            # print("gripper_2_channel", on)
        else:
            self.tools_dict["gripper_2"] = False
            # print("gripper_2_channel", on)

    def gripper_3_channel(self, on):
        if on:
            self.tools_dict["gripper_3"] = True
            # print("gripper_3_channel", on)
        else:
            self.tools_dict["gripper_3"] = False
            # print("gripper_3_channel", on)

    def throttle_channel(self, pwm):   
        # print("throttle_channel", pwm)     
        self.set_rc_pwm(3, pwm)

    def forward_channel(self, pwm):
        # print("forward_channel", pwm)
        self.set_rc_pwm(5, pwm)

    def arm_disarm(self, on):
        # if on:
        #     self.master.arducopter_arm()
        # else:
        #     self.master.arducopter_disarm()
            
        pass
    # def disarm(self):
    #     self.master.arducopter_disarm()
    #     pass

    def set_alt_hold(self, mode = None):

        # if mode not in self.master.mode_mapping():
        #  print('Unknown mode : {}'.format(mode))
        #  print('Try:', list(self.master.mode_mapping().keys()))
        # sys.exit(1)

        # mode_id = self.master.mode_mapping()["ALT_HOLD"]

        # self.master.mav.set_mode_send(
        # self.master.target_system,
        # mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        # mode_id)
        pass
    def set_manual(self, mode = None):
        # print("set_manual")

        # if mode not in self.master.mode_mapping():
        #  print('Unknown mode : {}'.format(mode))
        #  print('Try:', list(self.master.mode_mapping().keys()))
        # sys.exit(1)

        # mode_id = self.master.mode_mapping()["MANUAL"]

        # self.master.mav.set_mode_send(
        # self.master.target_system,
        # mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        # mode_id)
        pass
    def set_stabilize(self, mode = None):
        # print("set_stabilize")

        # if mode not in self.master.mode_mapping():
        #  print('Unknown mode : {}'.format(mode))
        #  print('Try:', list(self.master.mode_mapping().keys()))
        # sys.exit(1)

        # mode_id = self.master.mode_mapping()["STABILIZE"]

        # self.master.mav.set_mode_send(
        # self.master.target_system,
        # mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        # mode_id)
        pass

    def process_message(self, msg):
        for key in self.channels:
            if key in msg:
                self.channels[key](msg[key])

        self.yaw_channel(self.yaw)
        
        # serialized_dict = json.dumps(self.tools_dict)
        
        # if serialized_dict != self.old_message:
        #     self.old_message = serialized_dict
        #     self.client.send(serialized_dict.encode('utf-8'))
        

if __name__ == "__main__":
    rov_controller = ROVController()
    joystick = JoystickHandler()
    while True:
        joystick.handle_joy()
        msg = joystick.print_results()
        # print(msg)
        rov_controller.process_message(msg)



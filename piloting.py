from pymavlink import mavutil 
import serial
import socket
import sys
from communication.socket.client import ClientSocket
import json
from joystick.JoystickHandler import JoystickHandler

max_pwm = 1800
min_pwm = 1200
gripper_1 = 0 #pin
gripper_2 = 0 #pin
gripper_3 = 0 #pin
gripper_on = 5000
gripper_off = 0


class ROVController:
    def __init__(self):
        # self.master = mavutil.mavlink_connection("udp:" + "192.168.33.100" + ":" + str(14550), 115200)
        # self.master.wait_heartbeat()
        self.client = ClientSocket("192.168.33.1", 4096)
        self.client.connect()
        self.old_message = ""

        self.tools_dict = {
            
            "gripper_1": False,
            "gripper_2": False,
            "gripper_3": False
        }

        self.channels = {
            "a": self.throttle_channel, 
            "b": self.yaw_channel,
            "c": self.lateral_channel,
            "d": self.forward_channel,
            "e": self.gripper_1_channel,
            "f": self.gripper_2_channel,
            "g": self.gripper_3_channel,
            "H": self.arm,
            "I": self.disarm,
            "j": self.set_flight_mode
        }

    def set_rc_pwm(self, channel, pwm):
        # master.mav.rc_channels_override_send(
        #     master.target_system,
        #     master.target_component,
        #     pwm,
        #     channel
        # )
        pass

    def set_servo_pwm(self, servo, pwm):
        # master.mav.command_long_send(
        #     master.target_system,
        #     master.target_component,
        #     mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        #     0,
        #     servo,
        #     pwm,
        #     0, 0, 0, 0, 0
        # ) 
        pass

    def yaw_channel(self, pwm):
        self.set_rc_pwm(4, pwm)

    def lateral_channel(self, pwm):
        self.set_rc_pwm(2, pwm)

    def gripper_1_channel(self, on):
        if on:
            self.tools_dict["gripper_1"] = True
        else:   
            self.tools_dict["gripper_1"] = False

    def gripper_2_channel(self, on):
        if on:
            self.tools_dict["gripper_2"] = True
        else:
            self.tools_dict["gripper_2"] = False

    def gripper_3_channel(self, on):
        if on:
            self.tools_dict["gripper_3"] = True
        else:
            self.tools_dict["gripper_3"] = False

    def throttle_channel(self, pwm):        
        self.set_rc_pwm(3, pwm)

    def forward_channel(self, pwm):
        self.set_rc_pwm(5, pwm)

    def arm(self):
        # master.arducopter_arm()
        pass    

    def disarm(self):
        # master.arducopter_disarm()
        pass

    def set_flight_mode(self, mode):

        # if mode not in master.mode_mapping():
        #  print('Unknown mode : {}'.format(mode))
        #  print('Try:', list(master.mode_mapping().keys()))
        # sys.exit(1)

        # mode_id = master.mode_mapping()[mode]

        # master.mav.set_mode_send(
        # master.target_system,
        # mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        # mode_id)
        pass 

    def process_message(self, msg):
        for key in self.channels:
            if key in msg:
                self.channels[key](msg[key])
        
        serialized_dict = json.dumps(self.tools_dict)
        
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

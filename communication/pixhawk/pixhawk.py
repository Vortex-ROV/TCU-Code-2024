from pymavlink import mavutil
import sys
import time
import serial.tools.list_ports

from communication.messages import Message

class Pixhawk:
    
    def __init__(self, ip_address, port, baudrate):
        # self.port = self.find_pixhawk_port()
        self.port = port
        self.master = mavutil.mavlink_connection("udp:" + ip_address + ":" + str(port), baudrate)
        
        try:
            self.master.wait_heartbeat()
        except Exception as e:
            print(e)

        print("heartbeat received")

        self.set_max_motor_pwm(1800)
        self.set_min_motor_pwm(1200)
        
    def find_pixhawk_port(self):
        ports = serial.tools.list_ports.comports()
        # print(port.description) 
        for port in ports:
            print(port.description)
            if "Pixhawk" in port.description:  # Check if the description contains "Pixhawk"
                return port.device  # Return the port name if Pixhawk is found
        raise Exception  # Return None if Pixhawk is not found
    
    def heartbeat(self):
        while True : 
                self.master.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
                            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
                            mavutil.mavlink.MAV_MODE_FLAG_TEST_ENABLED,
                            0, 0)
            # print('heartbeat')
        
                time.sleep(1)
            
            
        
    def set_gripper_light_pwm(self, *msg):
        dic = {0 : 0,
        '0': 0,
           'L': '01',
           'R': '10',
           1:5000,
           'O':'00',
           'H':1800}
        self.master.set_servo(11,dic[msg[0]])
        self.master.set_servo(12,dic[msg[1]])
        self.master.set_servo(9,dic[msg[2]])
        self.master.set_servo(13,int(dic[msg[3]][0])*5000)
        self.master.set_servo(14,int(dic[msg[3]][1])*5000)
        self.master.set_servo(10,5000)
        
        
    def set_direction_channel_pwm(self, channel3,channel4,channel5,channel6):
        # Create an array to hold the RC channel values
        # print(channel3 , channel4 )
        rc_channel_values = [1500, 1500,channel3,channel4,channel5,channel6, 65535, 65535, 65535]

        # Send the RC channel override command
        self.master.mav.rc_channels_override_send(
            self.master.target_system,
            self.master.target_component,
            *rc_channel_values
                               )
    
    def arm(self):
        self.master.arducopter_arm()
        
    def disarm(self):   
        self.master.arducopter_disarm()
    
    def set_flight_mode(self,mode_char):
        # mapping character to mode name 
        mode = {
            'M': 'MANUAL',
            'S': 'STABILIZE',
            'A': 'ALT_HOLD'
        }
        
        modeName = mode.get(mode_char)
        # print("mode name:" , modeName )
        if modeName not in self.master.mode_mapping():
        
            print('Unknown mode : {}'.format(modeName))
            print('Try:', list(self.master.mode_mapping().keys()))
            sys.exit(1)
        
        mode_id = self.master.mode_mapping()[modeName]
        # print("ID:",mode_id)
        self.master.mav.set_mode_send(
    self.master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id)
        
    def set_max_motor_pwm(self,max=1800):
        #This sets the max PWM value in microseconds that will ever be output to the motors
        self.master.mav.param_set_send(
        self.master.target_system, self.master.target_component,
        b'MOT_PWM_MAX',
        max,
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32
    )
        
    def set_min_motor_pwm(self,min = 1200):
        #This sets the max PWM value in microseconds that will ever be output to the motors
        self.master.mav.param_set_send(
        self.master.target_system, self.master.target_component,
        b'MOT_PWM_MIN',
        min,
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32
     )
    
    def flight_mode_running_now(self):
        # Wait for a heartbeat message from the Pixhawk
        heartbeats = self.master.recv_match(type='HEARTBEAT', blocking=True)
        # Retrieve the flight mode from the heartbeat message
        mode = mavutil.mode_string_v10(heartbeats)
        # Print the current flight mode
        print("Flight mode:", mode)
        time.sleep(0.01)
        
    def control_pixhawk(self, message):
        """
        Parses the input message and sends the corresponding commands to the Pixhawk.

        :param message: A 25-character string representing control signals for throttle, yaw,
                        forward/backward, lateral movement, grippers, light, arm/disarm, flight mode,
                        and throttle gain.
        """
        
        self.set_direction_channel_pwm(message.get_value("throttle"), message.get_value("yaw"), message.get_value("forward"), message.get_value("lateral"))
        self.set_gripper_light_pwm(message.get_value("gripper_1"), message.get_value("gripper_2"), message.get_value("light"), message.get_value("rotating_gripper"))

        # if int(message[20]) == 1:
        #     self.Set_MAX_MOTOR_PWM(1750)
        #     self.Set_MIN_MOTOR_PWM(1250)
        # else:
        #     self.Set_MAX_MOTOR_PWM(1800)
        #     self.Set_MIN_MOTOR_PWM(1200)
        
        if message.get_value("armed"):
            self.arm()
        else:
            self.disarm()
        
        self.set_flight_mode(message.get_value("flight_mode"))

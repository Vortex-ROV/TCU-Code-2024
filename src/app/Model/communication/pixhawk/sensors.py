# Import mavutil
from pymavlink import mavutil
from communication.messages import SensorMessage

class SensorsCollector:
    """
    This class collects sensor data from the Pixhawk flight controller using the MAVLink protocol.
    It can collect IMU, pressure, depth, and heading data.
    """

    def __init__(self, master: mavutil.mavfile):
        """
        Initializes the SensorsCollector with the MAVLink master connection and requests data at a specified interval.
        
        :param master: MAVLink connection instance (mavutil.mavfile).
        """
        self.master = master

        self.__message = SensorMessage()

        # Request data from Pixhawk at defined intervals
        self.request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, 1)
        self.request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_VFR_HUD, 1000)

    def get_imu(self) -> str:
        """
        Retrieves IMU data from the Pixhawk.
        
        :return: IMU data as a concatenated string of accelerometer and gyroscope values, each padded to 6 bytes.
        """
        msg = self.master.recv_match(type="SCALED_IMU2")
        if not msg:
            return None

        imu_dic = msg.to_dict()
        imu_values = [imu_dic["xacc"], imu_dic["yacc"], imu_dic["zacc"], imu_dic["xgyro"], imu_dic["ygyro"], imu_dic["zgyro"]]

        # Pad each IMU value to 6 bytes
        imu_values = [self.__zfill(str(imu_values[i])) for i in range(len(imu_values))]
        
        # Convert the list to a single string
        imu_values = ''.join(map(str, imu_values))

        # Store the last IMU values
        self.prev_imu_reading: str = imu_values

        return imu_values

    def get_scaled_pressure2(self):
        """
        Retrieves scaled pressure and temperature data from the Pixhawk.
        
        :return: A list of pressure and temperature readings, each padded to 6 bytes.
        """
        msg = self.master.recv_match(type="SCALED_PRESSURE2")
        if not msg:
            return None

        pressure_dic = msg.to_dict()
        
        # Process pressure value
        pressure_value: float = pressure_dic["press_abs"] / 1000

        # Process temperature value
        temperature_value: float = pressure_dic["temperature"] / 100

        return [pressure_value, temperature_value]

    # def get_scaled_pressure3(self) -> str:
    #     """
    #     Retrieves temperature data from a secondary pressure sensor on the Pixhawk.
        
    #     :return: Temperature value as a 6-byte string.
    #     """
    #     msg = self.master.recv_match(type="SCALED_PRESSURE3")
    #     if not msg:
    #         return None

    #     temp_value: float = round(msg.to_dict()["temperature"], 1) / 100
    #     temp_value = self.__zfill(str(temp_value))

    #     # Store the last temperature reading
    #     self.prev_temp_reading = temp_value

    #     return temp_value

    def get_depth(self) -> float:
        """
        Retrieves the current depth of the vehicle from the Pixhawk.
        
        :return: Depth value as a 6-byte string.
        """
        msg = self.master.recv_match(type="GLOBAL_POSITION_INT")
        if not msg:
            return None

        return msg.to_dict()["relative_alt"] / 1000.0

    def get_heading(self) -> int:
        """
        Retrieves the current heading of the vehicle from the Pixhawk.
        
        :return: Heading value as a 3-byte string.
        """
        msg = self.master.recv_match(type="VFR_HUD")
        if not msg:
            return None

        return msg.to_dict()["heading"]

    def request_message_interval(self, message_id: int, frequency_hz: float):
        """
        Requests messages from the Pixhawk at a specified frequency.
        
        :param message_id: MAVLink message ID to request.
        :param frequency_hz: Frequency in Hz at which the message should be sent.
        """
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
            message_id,  # The MAVLink message ID
            1e6 / frequency_hz,  # Interval in microseconds
            0, 0, 0, 0,  # Unused parameters
            0  # Target address: 0 (default) for flight stack
        )

    def read_sensors(self) -> SensorMessage:
        """
        Retrieves all sensor readings (pressure, temperature, depth, and heading) and concatenates them into a single string.
        
        :return: Concatenated string of sensor readings.
        """

        readings = self.get_scaled_pressure2()
        if readings:
            self.__message.set_value("pressure", readings[0])
            self.__message.set_value("temperature", readings[1])

        # Append depth reading
        depth_reading = self.get_depth()
        if depth_reading:
            self.__message.set_value("depth", depth_reading)

        # Append heading reading
        heading_reading = self.get_heading()
        if heading_reading:
            self.__message.set_value("heading", heading_reading)

        return self.__message
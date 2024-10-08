from PyQt5.QtCore import QThread, pyqtSignal
from communication.client import ClientSocket
import time


class CompanionLink(QThread):
    sensors_to_gui_signal = pyqtSignal(bytes)
    connected_signal = pyqtSignal(bool)

    def __init__(self, address="192.168.33.1", port=4096, buffer_size=51):
        super().__init__()

        self.client = ClientSocket(address, port, self.connected_signal)

        self.__port = port
        self.__buffer_size = buffer_size

    def __recieve_sensors_reading(self):
        recieved_sensors = self.client.receive(self.__buffer_size)
        # print(recieved_sensors)
        return recieved_sensors

    def send_control_commands(self, data):
        self.client.send(data)

    def change_buffer_size(self, buff_size):
        self.__buffer_size = buff_size

    def connect_sensors_to_gui_signal(self, slot):
        self.sensors_to_gui_signal.connect(slot)

    def connect_client_signal(self, slot):
        self.connected_signal.connect(slot)

    def run(self):
        self.client.connect()
        print("connected to nvidia")

        while True:
            received_sensors = self.__recieve_sensors_reading()

            if received_sensors is not None:
                self.sensors_to_gui_signal.emit(received_sensors)
            # time.sleep(1)
        # t = 0
        # while True:
        #     if time() - t >= 1:
        #         received_sensors = '{"IMU": 31, "Bar30": 70, "Temp": 10}'
        #         if received_sensors is not None:
        #             self.__sensors_to_gui_signal.signal.emit(received_sensors.encode())
        #         t = time()

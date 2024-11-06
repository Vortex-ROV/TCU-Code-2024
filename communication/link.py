from communication.socket.client import ClientSocket
from communication.messages import Message, SensorMessage
from communication.pixhawk.pixhawk import Pixhawk
from communication.pixhawk.sensors import SensorsCollector

class CompanionLink:
    def __init__(self, address: str = "192.168.33.1", port: int = 4096):
        self.__client = ClientSocket(address, port)
        self.__buffer_size = len(SensorMessage().bytes())

    def control_pixhawk(self, message: Message) -> None:
        self.__client.send(message)

    def collect_sensors(self) -> SensorMessage:
        return SensorMessage(self.__client.receive(self.__buffer_size))
        
        
class MavproxyLink:
    def __init__(self, ip_address: str = "192.168.33.100", port: int = 14550, baudrate: int = 115200) -> None:
        self.__pixhawk = Pixhawk(ip_address, port, baudrate)
        self.__sensors_collector = SensorsCollector(self.__pixhawk.master)

    def control_pixhawk(self, message: Message) -> None:
        self.__pixhawk.control_pixhawk(message)

    def collect_sensors(self) -> SensorMessage:
        return self.__sensors_collector.read_sensors()


def main():
    # link = CompanionLink()
    link = MavproxyLink()
    while True:
        sensors = link.collect_sensors()
        print(sensors)
        link.control_pixhawk()
        break

if __name__ == "__main__":
    main()

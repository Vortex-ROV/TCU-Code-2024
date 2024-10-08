import socket
from PyQt5.QtCore import pyqtSignal, QObject 
import time

class ClientSocket(QObject):
    connected_signal = pyqtSignal(bytes)
    def __init__(self, address: str, port: int, connected_signal):
        self.__address = address
        self.__port = port

        self.__connected_signal = connected_signal

    def __del__(self):
        self.__socket.close()

    def connect(self):
        self.__connected_signal.emit(False)
        while True:
            try:
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__socket.connect((self.__address, self.__port))
                self.__socket.setblocking(False)
                print("connected to server succesfully")
                self.__connected_signal.emit(True)
                return
            except Exception as e:
                # print(e)
                # print("waiting for server")
                continue

    def receive(self, buffer_size: int):
        try:
            received = self.__socket.recv(buffer_size)
            if received is not None and len(received) != 0:
                return received
            raise socket.error
        except socket.error as e:
            # handle receive not ready
            if e.errno == 10035:
                return
            print(e)
            self.__socket.close()
            self.connect()
        
    def send(self, data: bytes):
        try:
            self.__socket.send(data)
        except socket.error as e:
            if e.errno == 10057:
                return
            print(e)
            self.__socket.close()
            self.connect()
        except AttributeError:
            pass

    def connect_signal(self, slot):
        self.connected_signal.connect(slot)


# client = ClientSocket('localhost', 12345)
# client.connect()

# t = 0
# while True:
#     received = client.receive(1024)
#     if received is not None and len(received) != 0:
#         print(received)
#     if time.time() - t >= 1:
#         client.send(b'{"temp": 20, "IMU": 30}')
#         t = time.time()
    
    # if received is not None and len(received) != 0:
    #     print("recieved a message from surface: ",received)
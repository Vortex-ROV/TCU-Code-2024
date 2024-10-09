import socket

class ClientSocket:
    def __init__(self, address: str, port: int):
        self.__address = address
        self.__port = port

    def __del__(self):
        self.__socket.close()

    def connect(self):
        while True:
            try:
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__socket.connect((self.__address, self.__port))
                self.__socket.setblocking(False)
                print("connected to server succesfully")
                return
            except Exception as e:
                print(e)
                print("waiting for server")
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

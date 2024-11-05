import socket

class ServerSocket:
    def __init__(self, port: int):
        self.__welcoming_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__welcoming_socket.bind(('localhost', port))
        self.__welcoming_socket.listen()

    def __del__(self):
        self.__welcoming_socket.close()
        self.__client_socket.close()

    def accept(self):
        print("waiting for client")
        self.__client_socket, _ = self.__welcoming_socket.accept()
        self.__client_socket.setblocking(False)
        print("connected to client")

    def receive(self, buffer_size: int):
        try:
            received = self.__client_socket.recv(buffer_size)
            if received is not None and len(received) != 0:
                return received
            raise socket.error
        except socket.error as e:
            # handle receive not ready
            if e.errno == 10035:
                return
            print(e)
            self.__client_socket.close()
            self.accept()

        
    def send(self, data: bytes):
        try:
            self.__client_socket.send(data)
        except socket.error as e:
            print(e)
            self.__client_socket.close()
            self.accept()
        except AttributeError as e:
            pass


server = ServerSocket(12345)
server.accept()

t = 0
while True:
    received = server.receive(1024)
    if received is not None and len(received) != 0:
        print(received)
# server = ServerSocket(12345)
# server.accept()

# t = 0
# while True:
#     received = server.receive(1024)
#     if received is not None and len(received) != 0:
#         print(received)

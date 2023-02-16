import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '143.42.17.208'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.PICKLE_SIZE = 1024 * 16

    def get(self):
        return self.client.recv(self.PICKLE_SIZE)

    def send(self, data):
        try:
            self.client.send(data)
            return self.client.recv(self.PICKLE_SIZE)
        except socket.error as e:
            print(e)

import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '172.104.241.208'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.PICKLE_SIZE = 1024 * 32

    def get(self):
        return self.client.recv(self.PICKLE_SIZE)

    def send(self, data):
        try:
            self.client.send(data)
            return self.client.recv(self.PICKLE_SIZE)
        except socket.error as e:
            print(e)

class Go:
    def __init__(self):
        self.client_limit = 2
        self.time = 10
        self.tiles = [[0 for _ in range(19)] for _ in range(19)]
        self.clients_status = []

from games.go import Go
# ^ path relative to lobby

class Game:
    def __init__(self, game_type):
        self.game_type = game_type
        self.clients = []
        if self.game_type == 'Go':
            self.game = Go()
        self.time_limit = self.game.time
        self.clients_limit = self.game.client_limit
        self.clients_times = [self.game.time for _ in range(len(self.clients))]
        self.clients_status = ['WAIT' for _ in range(len(self.clients))]
        self.game.clients_status = self.clients_status

    def update_time(self, client, time):
        self.clients_times[client] += time

    def update_move(self, move, client, time):  # turn it to return list with updates tiles
        try:
            if self.game.tiles[move[0]][move[1]] == 0:
                self.game.tiles[move[0]][move[1]] = client
                self.update_time(client-1, -time)     # -1 turn to set correct index, -time to subtract the time
                return True
            else:
                return False
        except IndexError:
            return False

    def update_status(self, client, status):
        self.clients_status[client] = status
        self.game.clients_status[client] = status

    def add_client(self, client_conn):
        self.clients.append(client_conn)
        self.clients_status.append('WAIT')
        self.clients_times.append(self.game.time)

    def remove_client(self, client):
        self.clients[client] = 0
        self.clients_status[client] = 'LEFT'
        self.clients_times[client] = 0

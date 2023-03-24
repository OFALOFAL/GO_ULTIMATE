from game import Game
from server_message_queue import server_q_put
import time

class Lobby:
    def __init__(self, client_conn, client_count, game_type, client_id, players_limit, tiles_ammount):
        self.id = client_id
        self.clients = [
            {
                'conn': client_conn,
                'role': 'HOST',
                'id': 0,
                'turn': 0,
                'end_game': False,
                'hand_points': 0,
                'tile_points': 0
                #name: name TODO: add name
            }
        ]
        self.host = self.clients[0]
        self.client_count = client_count
        self.game_type = game_type
        self.game = Game(game_type, players_limit, tiles_ammount)
        self.times = [self.game.time * 60 for _ in self.clients]
        self.last_move_time = time.time()
        self.ready = False
        self.clients_times = self.game.time
        self.clients_limit = self.game.players_limit
        self.closed = False
        self.active_turn = 0

    def send_clients_info(self):
        ret = []
        for client in self.clients:
            try:
                ret.append(
                    {
                        'conn': client['conn'].getsockname(),
                        'role': client['role'],
                        'id': client['id'],
                        'turn': client['turn'],
                        'end_game': client['end_game'],
                        'hand_points': client['hand_points'],
                        'tile_points': client['tile_points']
                    }
                )
            except OSError:
                ret.append(0)
            except TypeError:
                ret.append(0)
        return ret

    def update_time(self, turn, end_time):
        self.times[turn] -= round(end_time - self.last_move_time, 2)
        self.last_move_time = time.time()

    def add_client(self, client_conn, role, turn):
        self.client_count += 1
        self.clients.append(
            {
                'conn': client_conn,
                'role': role,
                'id': len(self.clients),
                'turn': turn,
                'end_game': False,
                'hand_points': 0,
                'tile_points': 0
            }
        )
        self.times = [self.game.time * 60 for _ in self.clients]

    def remove_client(self, client):
        self.client_count -= 1
        try:
            self.clients[client] = 0
            server_q_put('Removed client:', client)
            self.times[client] = self.game.time
        except IndexError:
            server_q_put('Client at:', client, 'is already deleted!')

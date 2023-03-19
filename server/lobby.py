from game import Game
from server_message_queue import server_q_put

class Lobby:
    def __init__(self, client_conn, client_count, game_type, client_id, players_limit, tiles_ammount):
        self.id = client_id
        self.clients = [
            {
                'conn': client_conn,
                'role': 'HOST',
                'id': 0,
                'turn': 0,
                'end_game': False
                #name: name TODO: add name
                #points: 0 TODO: add points from game (maybe in self.game is better)
            }
        ]
        self.host = self.clients[0]
        self.client_count = client_count
        self.game_type = game_type
        self.game = Game(game_type, players_limit, tiles_ammount)
        self.times = [self.game.time for _ in self.clients]
        self.ready = False
        self.clients_times = self.game.time
        self.clients_limit = self.game.players_limit
        self.closed = False
        self.active_turn = 0

    def add_client(self, client_conn, role, turn):
        self.client_count += 1
        self.clients.append(
            {
                'conn': client_conn,
                'role': role,
                'id': len(self.clients),
                'turn': turn,
                'end_game': False
            }
        )

    def remove_client(self, client):
        self.client_count -= 1
        try:
            self.clients[client] = 0
            server_q_put('Removed client:', client)
        except IndexError:
            server_q_put('Client at:', client, 'is already deleted!')

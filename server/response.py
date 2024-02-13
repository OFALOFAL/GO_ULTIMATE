class Response:
    def __init__(self,
                 # all:
                 game_type='', move=[], board=[], turn=0, addr='', is_ready=False, end_game_req=False, active_turn=False,
                 # window distinct request:
                 create_req=False, connect_req=False, start_game_req=False, lobby_wait=False, password='', client_is_ready=False, players_limit = 2,
                 tiles_amount = 18, game_update_req=False, move_req=False, client_name='',
                 # server distinct request:
                 validate_req=False, change_move_req=False, client_status=None, exit_req=False, server_update=False, game_summary = False, clients_info = [], times=[],
                 # host distinct request:
                 host=False, ban_clients=[], wait_for_clients=False,
                 ):
        # information distinguished by type
        request = is_ready or end_game_req \
                  or create_req or connect_req or start_game_req or lobby_wait or client_is_ready \
                  or validate_req or change_move_req or exit_req or server_update or game_summary \
                  or host or wait_for_clients or game_update_req or move_req
        self.type = {
            'request': request,
            'window': {
                'window': create_req or connect_req or start_game_req or lobby_wait or client_is_ready or (end_game_req and not server_update) or game_update_req or move_req,
                'client_addr': addr,
                'create_new_lobby_req': create_req,
                'connect_to_lobby_req': connect_req,
                'start_game_req': start_game_req,
                'lobby_wait': lobby_wait,
                'password': password,
                'players_limit': players_limit,
                'tiles_amount': tiles_amount,
                'game_update_req': game_update_req,
                'move_req': move_req,
                'end_game_req': end_game_req,
                'client_name': client_name
            },
            'server': {
                'server': validate_req or change_move_req or exit_req or is_ready or server_update or game_summary,
                'server_addr': addr,
                'client_status': client_status,
                'client_validation': validate_req,
                'change_move_request': change_move_req,
                'host_exit_request': exit_req,
                'server_update': server_update,
                'game_summary': game_summary,
                'clients_info': clients_info,
                'times': times
            },
            'host': {   # nescessery host information
                'host': host,
                'wait_for_clients': wait_for_clients,
                'ban_clients': ban_clients,
            }
        }

        # clean up useless information
        if host:
            self.type['server']['client_status'] = 'HOST'
        if self.type['server']['client_status'] != 'HOST':
            self.type['host'] = {'host': False}
        if self.type['window']['window']:
            self.type['server'] = {'server': False}
        elif self.type['server']['server']:
            self.type['window'] = {'window': False}
        if not self.type['server']['server'] and not self.type['window']['window']:
            self.type['server'] = {'server': False}
            self.type['window'] = {'window': False}

        # validate the message
        self.valid = True
        if not self.type['request']:
            if game_type != '':
                self.game_type = game_type
            else:
                print('Sending invalid response to:', addr)
                self.valid = False
        else:
            self.game_type = game_type

        # add content if valid
        if self.valid:
            if not (create_req and connect_req):
                self.move = move
                self.board = board
            self.turn = turn
            self.create_req = create_req
            self.connect_req = connect_req
            self.is_ready = is_ready or client_is_ready
            self.active_turn = active_turn
        else:
            return

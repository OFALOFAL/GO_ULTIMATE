class Response:
    def __init__(self,
                 # all:
                 game_type='', move=[], times=[], turn=0, addr='', is_ready=False, end_game_req=False, active_turn=False,
                 # client_del distinct request:
                 create_req=False, connect_req=False, start_game_req=False, lobby_wait=False, password='', client_is_ready=False, pause=False,
                 # server distinct request:
                 validate_req=False, change_move_req=False, client_status=None, exit_req=False, update=False,
                 # host distinct request:
                 host=False, clients=[], ban_clients=[], wait_for_clients=False,
                 ):
        # information distinguished by type
        request = is_ready or end_game_req \
                  or create_req or connect_req or start_game_req or lobby_wait or client_is_ready \
                  or validate_req or change_move_req or exit_req or update \
                  or host or wait_for_clients
        self.type = {
            'request': request,
            'client_del': {
                'client_del': create_req or connect_req or start_game_req or lobby_wait or client_is_ready or (end_game_req and not update),
                'client_addr': addr,
                'create_new_lobby_req': create_req,
                'connect_to_lobby_req': connect_req,
                'start_game_req': start_game_req,
                'lobby_wait': lobby_wait,
                'password': password
            },
            'server': {
                'server': validate_req or change_move_req or exit_req or is_ready or update,
                'server_addr': addr,
                'client_status': client_status,
                'client_validation': validate_req,
                'change_move_request': change_move_req,
                'host_exit_request': exit_req,
                'update': update
            },
            'host': {   # nescessery host information
                'host': host,
                'wait_for_clients': wait_for_clients,
                'clients': clients,
                'ban_clients': ban_clients
            }
        }

        # clean up useless information
        if host:
            self.type['server']['client_status'] = 'HOST'
        if self.type['server']['client_status'] != 'HOST':
            self.type['host'] = {'host': False}
        if self.type['client_del']['client_del']:
            self.type['server'] = {'server': False}
        elif self.type['server']['server']:
            self.type['client_del'] = {'client_del': False}
        if not self.type['server']['server'] and not self.type['client_del']['client_del']:
            self.type['server'] = {'server': False}
            self.type['client_del'] = {'client_del': False}

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
            self.times = times
            self.turn = turn
            self.create_req = create_req
            self.connect_req = connect_req
            self.is_ready = is_ready or client_is_ready
            self.end_game_req = end_game_req
            self.active_turn = active_turn
            self.board_update = [[[], ]]    # [[place], new sign]
        else:
            return

import sys

from response import Response
from network import Network
import pickle
import socket
from window import Window
from _thread import start_new_thread

password = 'qqwkkjhasfa198998j923r9u9823n89n9uw8nf923n9rfn9jnav038rn'

def update_board(n: Network, game_type, addr):
    response = Response(game_type, addr=addr, client_is_ready=True, game_update_req=True)
    return n.send(pickle.dumps(response))

def send_move(n: Network, game_type, move, turn, addr):
    response = Response(game_type, move=move, turn=turn, addr=addr, client_is_ready=True, move_req=True)
    msg = n.send(pickle.dumps(response))
    return msg
    # return n.send(pickle.dumps(response))

def create(n: Network, game_type, addr, players_limit = 2, tiles_ammount = 18, name=''):
    n.client.connect(n.addr)
    response = Response(game_type, create_req=True, addr=addr, password=password, players_limit=players_limit, tiles_amount=tiles_ammount, client_name=name)
    return n.send(pickle.dumps(response))

def connect(n: Network, game_type, addr, players_limit = 2, tiles_amount = 18, name=''):
    print(game_type, addr, players_limit, tiles_amount)
    try:
        n.client.connect(n.addr)
    except TimeoutError:
        return False
    except ConnectionRefusedError:
        return False
    except OSError:
        return False
    response = Response(game_type, connect_req=True, addr=addr, password=password, players_limit=players_limit, tiles_amount=tiles_amount, client_name=name)
    return n.send(pickle.dumps(response))

def dissconnect(n: Network):
    n.client.close()
    return Network()

def start(n: Network, addr):
    return pickle.loads(n.send(pickle.dumps(Response(start_game_req=True, addr=addr))))

def wait_for_lobby(n: Network):
    return pickle.loads(n.send(pickle.dumps(Response(lobby_wait=True))))

def wait_for_clients(n: Network):
    return pickle.loads(n.send(pickle.dumps(Response(host=True, wait_for_clients=True))))

def ban_clients(n: Network, clients):
    return pickle.loads(n.send(pickle.dumps(Response(host=True, ban_clients=clients))))

def send_end_game_req(n: Network):
    n.send(pickle.dumps(Response(end_game_req=True)))

window = Window()

if __name__ == '__main__':
    game_type = 'SANDBOX'
    IP_ADDR = socket.gethostbyname(socket.gethostname())
    network = Network()     # reset network
    run = True
    server_status = ''
    turn = -1
    window_info = None
    connected = False
    move = [False, []]
    board = [False, []]
    game_summary = False
    times = [False, []]
    host = False
    clients_info = []
    name = ''

    def connect_thread(players_limit, tiles_amount, name):
        # Using globals becouse thread can't return values
        global server_status
        global turn
        global window_info
        global connected
        global host
        global clients_info
        global network
        clients_info = []

        if not connect(network, game_type, IP_ADDR, players_limit, tiles_amount, name):
            print('Server Closed')
            server_status = 'CLOSED'
        else:
            server_status = 'CONNECTED'
            try:
                response = pickle.loads(network.get())
                print('Connected to server, my turn:', response.turn)
                turn = response.turn
                if response.type['host']['host']:
                    host = True
                    response = wait_for_clients(network)
                    clients_info = response.type['server']['clients_info']
                    while not len(clients_info) == players_limit:
                        response = wait_for_clients(network)
                        clients_info = response.type['server']['clients_info']
                    else:
                        connected = True
                        start_info = start(network, IP_ADDR)
                        clients_info = start_info.type['server']['clients_info']
                        print('started lobby')
                else:
                    response = wait_for_lobby(network)
                    clients_info = response.type['server']['clients_info']
                    while not response.is_ready:
                        pass
                    else:
                        connected = True
                        print('connected to lobby')
            except TypeError:
                network = dissconnect(network)
            except KeyboardInterrupt:
                network = dissconnect(network)
            except EOFError:
                network = dissconnect(network)

    def create_thread(players_limit, tiles_amount):
        # Using globals becouse thread can't return values
        global server_status
        global turn
        global window_info
        global connected
        global host
        global network
        global clients_info
        clients_info = []

        if not connect(network, game_type, IP_ADDR, players_limit, tiles_amount, name):
            print('Server Closed')
            server_status = 'CLOSED'
        else:
            server_status = 'CONNECTED'
            try:
                response = pickle.loads(network.get())
                print('Connected to server, my turn:', response.turn)
                turn = response.turn
                if response.type['host']['host']:
                    host = True
                    response = wait_for_clients(network)
                    clients_info = response.type['server']['clients_info']
                    while not len(clients_info) == players_limit:
                        response = wait_for_clients(network)
                        clients_info = response.type['server']['clients_info']
                    else:
                        connected = True
                        start_info = start(network, IP_ADDR)
                        clients_info = start_info.type['server']['clients_info']
                        print('started lobby')
                else:
                    network = dissconnect(network)
                    server_status = 'CLOSED'
            except TypeError:
                network = dissconnect(network)
            except KeyboardInterrupt:
                network = dissconnect(network)
            except EOFError:
                network = dissconnect(network)

    def _send_move():
        # Using globals becouse thread can't return values
        global connected
        global server_status
        global board
        global move
        global game_summary
        global times
        global clients_info
        global network

        response = send_move(network, game_type, value, turn, IP_ADDR)
        if response is None:
            server_status = 'DISCONNECTED'
        else:
            try:
                response = pickle.loads(response)
            except TypeError:
                connected = False
            except KeyboardInterrupt:
                connected = False
            except EOFError:
                connected = False
            if response.type['server']['server']:
                if response.type['server']['change_move_request']:
                    move = 'CHANGE_MOVE'
                elif response.type['server']['game_summary']:
                    board = [False, []]
                    game_summary = True
                    clients_info = response.type['server']['clients_info']
                else:
                    board = [True, response.board]
                    clients_info = response.type['server']['clients_info']
                    if len(response.type['server']['times']):
                        times = [True, response.type['server']['times']]
                    else:
                        times = [False]

    def _update_board():
        # Using globals becouse thread can't return values
        global connected
        global server_status
        global board
        global game_summary
        global times
        global clients_info
        global network

        response = update_board(network, game_type, IP_ADDR)
        if response is None:
            server_status = 'DISCONNECTED'
        else:
            try:
                response = pickle.loads(response)
            except TypeError:
                connected = False
            except KeyboardInterrupt:
                connected = False
            except EOFError:
                connected = False
            if response.type['server']['server']:
                if response.type['server']['game_summary']:
                    board = [False, []]
                    game_summary = True
                    clients_info = response.type['server']['clients_info']
                else:
                    board = [True, response.board]
                    clients_info = response.type['server']['clients_info']
                    if len(response.type['server']['times']):
                        times = [True, response.type['server']['times']]
                    else:
                        times = [False]


    while run:
        window_info, value = window.run(run, server_status, game_type, turn, host, move, board, times, game_summary, clients_info)
        if connected:
            if window_info == 'move':
                start_new_thread(_send_move, ())
            else:
                start_new_thread(_update_board, ())
        else:
            board = [False, []]
            times = [False, []]

        if window_info == 'run':
            run, game_type = value
        elif window_info == 'end_game_summary':
            game_summary = False
            network = dissconnect(network)
            board[0] = False
            times = [False, []]
            clients_info = []
            server_status = 'DISCONNECTED'
            connected = False
            run = value
        elif window_info == 'connect':
            game_summary = False
            game_type, players_limit, tiles_amount, name = value
            start_new_thread(connect_thread, (players_limit, tiles_amount, name))
        elif window_info == 'create':
            game_summary = False
            game_type, players_limit, tiles_amount = value
            start_new_thread(create_thread, (players_limit, tiles_amount, name))
        elif window_info == 'disconnect':
            network = dissconnect(network)
            board[0] = False
            times = [False, []]
            clients_info = []
            server_status = 'DISCONNECTED'
            connected = False
        elif window_info == 'END_GAME':
            start_new_thread(send_end_game_req, (network, ))
        elif window_info == 'BAN':
            start_new_thread(ban_clients, (network, [value]))
        elif window_info == 'move':
            if game_type == 'SANDBOX':
                move = ['MOVE', value]
        elif window_info == 'del':
            if game_type == 'SANDBOX':
                move = ['DEL', value]
        elif window_info == 'exit':
            sys.exit()
        run = value

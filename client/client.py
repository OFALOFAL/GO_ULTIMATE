from response import Response
from network import Network
import pickle
import socket
from window import Window
from _thread import start_new_thread

password = 'MKAMksj#4525kjmois563&*sf'

def update_board(n: Network, game_type, addr):
    response = Response(game_type, addr=addr, client_is_ready=True, game_update_req=True)
    return n.send(pickle.dumps(response))

def send_move(n: Network, game_type, move, time, turn, addr):
    response = Response(game_type, move=move, times=time, turn=turn, addr=addr, client_is_ready=True, move_req=True)
    msg = n.send(pickle.dumps(response))
    return msg
    # return n.send(pickle.dumps(response))

def create(n: Network, game_type, addr, players_limit = 2, tiles_ammount = 18):
    n.client.connect(n.addr)
    response = Response(game_type, create_req=True, addr=addr, players_limit=players_limit, tiles_amount=tiles_ammount)
    return n.send(pickle.dumps(response))

def connect(n: Network, game_type, addr, players_limit = 2, tiles_amount = 18):
    try:
        n.client.connect(n.addr)
    except TimeoutError:
        return False
    except ConnectionRefusedError:
        return False
    except OSError:
        return False
    response = Response(game_type, connect_req=True, addr=addr, password=password, players_limit=players_limit, tiles_amount=tiles_amount)
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
    return n.send(pickle.dumps(Response(end_game_req=True)))

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

    def connect_thread(players_limit, time):
        # Using globals becouse thread can't return values
        global server_status
        global turn
        global window_info
        global connected
        if not connect(network, game_type, IP_ADDR):
            print('Server Closed')
            server_status = 'CLOSED'
        else:
            server_status = 'CONNECTED'
            try:
                response = pickle.loads(network.get())
            except EOFError:
                dissconnect(network)
                server_status = 'CLOSED'
            print('Connected to:', response.type['server']['server_addr'], response.turn)
            turn = response.turn
            if response.type['host']['host']:
                try:
                    while not  len(wait_for_clients(network).type['host']['clients']) == players_limit:
                        pass
                    else:
                        connected = True
                        print('started lobby')
                        start_info = start(network, IP_ADDR)
                except:
                    server_status = 'CLOSED'
            else:
                try:
                    while not wait_for_lobby(network).is_ready:
                        pass
                    else:
                        connected = True
                        print('connected to lobby')
                except:
                    server_status = 'CLOSED'

    def _send_move(n: Network):
        # Using globals becouse thread can't return values
        global connected
        global server_status
        global board
        global move

        response = send_move(n, game_type, value, 0, turn, IP_ADDR)
        if response is None:
            server_status = 'CLOSED'
        else:
            try:
                response = pickle.loads(response)
            except TypeError:
                _connected = False
            except KeyboardInterrupt:
                _connected = False
            except EOFError:
                _connected = False
            if response.end_game_req:
                _server_status = 'END_GAME_REQ'
            elif response.type['server']['server']:
                if response.type['server']['host_exit_request']:
                    _connected = False
                    n = dissconnect(n)
                    _server_status = 'GAME_END'  # TODO: send summary of the game
                elif response.type['server']['change_move_request']:
                    _move = 'CHANGE_MOVE'
                else:
                    board = [True, response.board]

    def _update_board(n: Network):
        # Using globals becouse thread can't return values
        global connected
        global server_status
        global board

        response = update_board(n, game_type, IP_ADDR)
        if response is None:
            server_status = 'CLOSED'
        else:
            try:
                response = pickle.loads(response)
            except TypeError:
                _connected = False
            except KeyboardInterrupt:
                _connected = False
            except EOFError:
                _connected = False
            if response.end_game_req:
                _server_status = 'END_GAME_REQ'
            elif response.type['server']['server']:
                board = [True, response.board]


    while run:
        window_info, value = window.run(run, server_status, game_type, move, board)
        if connected:
            if window_info == 'move':
                start_new_thread(_send_move, (network, ))
            else:
                start_new_thread(_update_board, (network, ))
        else:
            board = [False, []]

        match window_info:
            case 'run':
                run = value
            case 'connect':
                game_type, players_limit, time = value
                start_new_thread(connect_thread, (players_limit, time))
            case 'disconnect':
                network = dissconnect(network)
                board[0] = False
                server_status = 'DISCONNECTED'
            case 'end_game_req':
                send_end_game_req(network)
            case 'move':
                if game_type == 'SANDBOX':
                    move = ['MOVE', value]
            case 'del':
                if game_type == 'SANDBOX':
                    move = ['DEL', value]
            case 'exit':
                break

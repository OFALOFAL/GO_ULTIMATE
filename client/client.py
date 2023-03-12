from response import Response
from network import Network
import pickle
import socket
from window import Window
from _thread import start_new_thread

password = 'MKAMksj#4525kjmois563&*sf'

def update_move(response: Response):
    pass

def send_move(n: Network, game_type, move, time, turn, addr):
    response = Response(game_type, move=move, times=time, turn=turn, addr=addr, client_is_ready=True)
    return n.send(pickle.dumps(response))

def create(n: Network, game_type, addr):
    n.client.connect(n.addr)
    response = Response(game_type, create_req=True, addr=addr)
    return n.send(pickle.dumps(response))

def connect(n: Network, game_type, addr):
    try:
        n.client.connect(n.addr)
    except TimeoutError:
        return False
    except ConnectionRefusedError:
        return False
    except OSError:
        return False
    response = Response(game_type, connect_req=True, addr=addr, password=password)
    return n.send(pickle.dumps(response))

def dissconnect(n: Network):
    n.client.close()
    return Network()

def start(n: Network):
    n.send(pickle.dumps(Response(start_game_req=True, turn=1, addr='START')))

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

    def connect_thread(players_limit, time):
        global server_status
        global turn
        global window_info
        global connected
        if not connect(network, game_type, IP_ADDR):
            print('Server Closed')
            server_status = 'CLOSED'
        else:
            response = pickle.loads(network.get())
            print('Connected to:', response.type['server']['server_addr'], response.turn)
            turn = response.turn
            if response.type['host']['host']:
                host = True
                try:
                    while len(wait_for_clients(network).type['host']['clients']) < players_limit:
                        pass
                except:
                    return
                start(network)
                server_status = 'CONNECTED'
                connected = True
            else:
                ready = False
                try:
                    while not ready:
                        wait = wait_for_lobby(network)
                        ready = wait.is_ready
                    server_status = 'CONNECTED'
                    connected = True
                except:
                    return
    move = [False, []]
    while run:
        window_info, value = window.run(run, server_status, game_type, move)
        if connected:
            response = send_move(network, game_type, value, 0, turn, IP_ADDR)
            if response is None:
                run = False
                move = [True, value]
                server_status = 'CLOSED'
            else:
                try:
                    response = pickle.loads(response)
                except TypeError:
                    break
                except KeyboardInterrupt:
                    break
                except EOFError:
                    break
                if not response.change_move_req:
                    move = [response.move, response.times]
                else:
                    move = [not response.change_move_req]
            if response.end_game_req:
                server_status = 'END_GAME_REQ'
            elif response.type['server']['server']:
                if response.type['server']['host_exit_request']:
                    network = dissconnect(network)
                    server_status = 'GAME_END'  # TODO: send summary of the game
                elif response.type['server']['change_move_request']:
                    move = 'CHANGE_MOVE'
        match window_info:
            case 'run':
                run = value
            case 'connect':
                game_type, players_limit, time = value
                start_new_thread(connect_thread, (players_limit, time))
            case 'move':
                if game_type == 'SANDBOX':
                    move = ['MOVE', value]
            case 'del':
                if game_type == 'SANDBOX':
                    move = ['DEL', value]
            case 'end_game_req':
                send_end_game_req(network)
            case 'exit':
                break

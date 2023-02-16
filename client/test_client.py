from response import Response
from network import Network
import pickle
import socket
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


run = True
end_game = False
get = True
def test_run(n: Network):
    global run
    global end_game
    global get
    try:
        if not connect(n, game_type, IP_ADDR):
            print('Server Closed')
        else:
            response = pickle.loads(n.get())
            print('Connected to:', response.type['server']['server_addr'], response.turn)
            turn = response.turn
            i, j = 0, 0
            if response.type['host']['host']:
                host = True
                try:
                    while len(wait_for_clients(n).type['host']['clients']) < 2:
                        pass
                except:
                    return
                start(n)
            else:
                ready = False
                try:
                    while not ready:
                        wait = wait_for_lobby(n)
                        ready = wait.is_ready
                except:
                    return

            while run:
                try:
                    if end_game:
                        response = send_end_game_req(n)
                    else:
                        response = send_move(n, game_type, [i, j], 1, turn, IP_ADDR)
                except KeyboardInterrupt:
                    pass
                if response is None:
                    print('Connection failed')
                    run = False
                    break
                else:
                    try:
                        response = pickle.loads(response)
                    except TypeError:
                        break
                    except KeyboardInterrupt:
                        break
                    except EOFError:
                        break
                    if not response.valid:
                        print('Connection failed, invalid request')
                        print('Host closed lobby')
                        n = dissconnect(n)
                        break
                if response.end_game_req:
                    send_end_game_req(n)
                elif response.type['server']['server']:
                    if response.type['server']['host_exit_request']:
                        print('Host closed lobby')
                        n = dissconnect(n)
                        break
                    elif response.type['server']['change_move_request']:
                        i += turn
                        j = i//2
                        # print('changing move to:', [i, j])
                    # elif response.active_turn != turn:
                    #     print('Wait for your turn')
                    # else:
                    #     print('Got:', response.move, ' from:', response.active_turn)
                else:
                    return
    except ConnectionRefusedError:
        print('Server Closed')
    except KeyboardInterrupt:
        return

def client_command_line(n: Network):
    global run
    global end_game
    global get
    while get:
        try:
            get_command = input()
            print('NOT OK')
        except UnicodeDecodeError:
            return
        if get_command == 'Q':
            run = False
        if get_command == 'E':
            end_game = True
            get = False

if __name__ == '__main__':
    game_type = 'Go'
    IP_ADDR = socket.gethostbyname(socket.gethostname())
    network = Network()     # reset network
    start_new_thread(client_command_line, (network, ))
    test_run(network)

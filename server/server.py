import socket
import os
import signal
import time
from _thread import start_new_thread
from response import Response
from lobby import Lobby
import pickle
from server_message_queue import server_q_put, get_q_size

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = '192.168.56.1'
port = 5555
server_ip = socket.gethostbyname(server)

PICKLE_SIZE = 1024 * 16


try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
server_q_put("Waiting for a connection, Server Started.")

connected = set()
lobbies = []

running = True
password = 'MKAMksj#4525kjmois563&*sf'

def threaded_client(conn, addr):
    try:
        conn.send(pickle.dumps(Response(validate_req=True, addr=addr)))
    except ConnectionResetError:
        return
    try:
        user_info = pickle.loads(conn.recv(PICKLE_SIZE))
    except EOFError:
        server_q_put('Client:', addr, 'failed to validate: invalid response')
        conn.send(pickle.dumps(Response(addr=addr)))
        return
    except pickle.UnpicklingError:
        server_q_put('Client:', addr, 'failed to validate: invalid response')
        conn.send(pickle.dumps(Response(addr=addr)))
        return
    except ConnectionResetError:
        server_q_put('Client:', addr, 'closed connection')
        return
    try:
        if user_info.type['client']['password'] != password:
            server_q_put('Client:', user_info.type['client']['client_addr'], 'failed to validate: wrong password')
            conn.send(pickle.dumps(Response(addr=addr)))   # send invalid response back to client
            return
    except KeyError:
        server_q_put('Client failed to validate message type')
    turn = 0
    lobby = Lobby   # lobby string which will be replaced by connection or new lobby
    host = False
    strikes = 0  # counts how many times user sended invalid response for longer bans
    if user_info.connect_req:
        is_available = False
        for l in lobbies:
            if l.game_type == user_info.game_type and l.game.tiles_ammount == user_info.type['client']['tiles_amount'] and l.client_count < l.clients_limit and not l.closed:
                is_available = True
                turn = 0
                replaced = False
                for x, c in enumerate(l.clients):
                    if not c['left']:
                        turn += 1
                    else:
                        replaced = True
                        l.replace_client(conn, 'CLIENT', x)
                if not replaced:
                    l.add_client(conn, 'CLIENT', turn)
                lobby = l
                conn.send(pickle.dumps(Response(game_type=user_info.game_type, turn=turn, server_update=True)))   # send clients turn
                server_q_put('Connected to lobby:', lobby.id)
                break
        if not is_available:
            user_info.connect_req = False
            user_info.create_req = True

    if user_info.create_req:
        lobbies.append(Lobby(conn, user_info.game_type, len(lobbies), user_info.type['client']['players_limit'], user_info.type['client']['tiles_amount']))
        lobby = lobbies[-1]
        lobby.active_turn = turn
        conn.send(pickle.dumps(Response(user_info.game_type, addr=addr, turn=turn, host=True, server_update=True)))   # send clients turn
        host = True
        server_q_put('Created new lobby:', lobby.id)

    client_id = turn    # set clients id to his turn

    while True:
        if not running:
            conn.send(pickle.dumps(Response(addr=addr, server_update=True)))
            return
        try:
            data = pickle.loads(conn.recv(PICKLE_SIZE))
            if not data:
                break
            elif data.type['host']['host']:
                if data.type['host']['wait_for_clients']:
                    response = Response(game_type=user_info.game_type, host=True, clients_info=lobby.send_clients_info(), times=lobby.times, server_update=True)
                    conn.send(pickle.dumps(response))     # send update to host
                elif len(data.type['host']['ban_clients']) > 0:
                    for ban in data.type['host']['ban_clients']:
                        try:
                            lobby.remove_client(ban)
                        except:
                            pass
            elif data.type['client']['client']:
                if data.type['client']['lobby_wait']:
                    conn.send(pickle.dumps(Response(is_ready=lobby.ready, clients_info=lobby.send_clients_info(), server_update=True)))    # send update to user
                elif data.type['client']['start_game_req']:     # update server
                    lobby.ready = True    # start lobby
                    lobby.clients_limit = len(lobby.clients) - 1    # cut new joining players
                    lobby.last_move_time = time.time()
                    conn.send(pickle.dumps(Response(server_update=True, clients_info=lobby.send_clients_info())))
                    server_q_put('Lobby', lobby.id, 'is ready; started by:', data.type['client']['client_addr'])


                if data.end_game_req:
                    for client in lobby.clients:
                        if client['conn'] == conn:
                            client['end_game'] = not client['end_game']
                elif lobby.ready and data.type['client']['move_req']:
                    if data.turn == lobby.active_turn:
                        if lobby.game.add_move([data.turn, data.move]):
                            update_time = False # this decides if time is updated, time doesn't have to be updated in sending move as the update board is sended constantly anyway
                            server_q_put('Client:', data.type['client']['client_addr'],': | turn:', data.turn, '| move:',data.move)
                            turn = data.turn
                            if turn < lobby.clients_limit:
                                next_turn = turn+1
                            else:
                                next_turn = 0
                            lobby.active_turn = next_turn
                            for x, client in enumerate(lobby.clients):
                                client['hand_points'] = lobby.game.hand_points[x]
                                client['tile_points'] = lobby.game.tile_points[x]
                                if not client['left']:
                                    try:
                                        response = Response(board=lobby.game.tiles, active_turn=lobby.active_turn, server_update=True, times=lobby.times, clients_info=lobby.send_clients_info())
                                        client['conn'].send(pickle.dumps(response))
                                        update_time = True
                                    except ConnectionResetError:
                                        server_q_put('update')
                                        lobby.active_turn = turn
                                        update_time = False
                                    except OSError:
                                        lobby.active_turn = turn
                                        update_time = False
                                else:
                                    update_time = False
                            if update_time:
                                lobby.update_time(turn, time.time())
                            turn = next_turn
                        else:
                            server_q_put('client:', data.type['client']['client_addr'],': | turn:', data.turn, '| invalid_move:',data.move)
                    else:
                        server_q_put('turn:', lobby.active_turn, 'got:', data.turn)
                elif lobby.ready and data.type['client']['game_update_req']:
                    lobby.update_time(lobby.active_turn, time.time())
                    response = Response(board=lobby.game.tiles, active_turn=lobby.active_turn, times=lobby.times, server_update=True, clients_info=lobby.send_clients_info())
                    conn.send(pickle.dumps(response))

                if lobby.game_type in ['GO | 5', 'GO | 10', 'GO | 30']:
                    for t in lobby.times:
                        print(lobby.times)
                        if t <= 1:
                            server_q_put('Closing lobby:', lobby.id)
                            conn.send(pickle.dumps(Response(board=lobby.game.tiles, game_summary=True, times=lobby.times, clients_info=lobby.send_clients_info())))

                if lobby.client_count == 1 and not host:
                    break

                temp = []
                for client in lobby.clients:
                    temp.append(client['end_game'])
                end_game = all(temp)
                if end_game:
                    server_q_put('Closing lobby:', lobby.id)
                    conn.send(pickle.dumps(Response(board=lobby.game.tiles, game_summary=True, times=lobby.times, clients_info=lobby.send_clients_info())))

            else:
                server_q_put('Invalid response from:', addr)
                # server_q_put(*[str(value)+':\n\t'+str(data.type['client'][value])+'\n' for value in data.type['client']])
                # server_q_put(*[str(value)+':\n\t'+str(data.type['server'][value])+'\n' for value in data.type['server']])
                # server_q_put(*[str(value)+':\n\t'+str(data.type['host'][value])+'\n' for value in data.type['host']])
                break

            if strikes == 30:
                server_q_put('Client:', addr, 'got cicked for spamming')
                conn.send(pickle.dumps(Response(addr=addr)))  # send invalid respond to stop user from spaming
                return

        except pickle.UnpicklingError as e:
            server_q_put("Couldn't load data:", e, 'UERR')
        except ConnectionAbortedError as e:
            server_q_put('Client:', addr, 'closed connection', e, 'CAERR')
            break
        except ConnectionResetError as e:
            server_q_put('Client:', addr, 'closed connection', e, 'CRERR')
            break
        except EOFError as e:
            server_q_put('Client:', addr, 'closed connection', e, 'EOFERR')
            break

    server_q_put("Lost connection with client:", user_info.type['client']['client_addr'], lobby.clients[client_id-1]['role'])
    lobby.remove_client(client_id)
    if lobby.client_count == 1:  # if only 1 is playing
        for client in lobby.clients:
            if not client['left']:
                client['conn'].send(pickle.dumps(Response(board=lobby.game.tiles, game_summary=True, times=lobby.times, clients_info=lobby.send_clients_info())))
        lobbies.remove(lobby)
    conn.close()

def handle_clients():
    server_q_put('Server Opened')
    while running:
        try:
            conn, addr = s.accept()
            server_q_put("Connected to:", addr)
            start_new_thread(threaded_client, (conn, addr))
        except KeyboardInterrupt:
            pass
    server_q_put('Server Closed')

def server_command_line():
    global running
    get = True
    get_command = ''
    while get:
        if get_q_size() == 0:
            try:
                get_command = input('\n↓')
            except UnicodeDecodeError:
                return
        if get_command == 'Q':
            os.kill(os.getpid(), signal.SIGTERM)
        elif get_command == 'B':
            running = False
        elif get_command == 'S':
            handle_clients()
        elif get_command == 'R':
            running = False
            handle_clients()
        elif get_command == 'REM':
            pass

start_new_thread(server_command_line, ())
handle_clients()

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
    if user_info.type['client']['password'] != password:
        server_q_put('Client:', user_info.type['client']['client_addr'], 'failed to validate: wrong password')
        conn.send(pickle.dumps(Response(addr=addr)))   # send invalid response back to client
        return
    turn = 1
    lobby = Lobby   # lobby string which will be replaced by connection or new lobby
    host = False
    strikes = 0  # counts how many times user sended invalid response for longer bans
    if user_info.connect_req:
        is_available = False
        for l in lobbies:
            if l.game_type == user_info.game_type and l.client_count < l.clients_limit and not l.closed:
                is_available = True
                turn = len(l.clients) + 1
                l.add_client(conn, 'USER', turn)
                lobby = l
                conn.send(pickle.dumps(Response(user_info.game_type, addr=addr, turn=turn, update=True)))   # send clients turn
                server_q_put('Connected to lobby:', lobby.id)
                break
        if not is_available:
            user_info.connect_req = False
            user_info.create_req = True

    if user_info.create_req:
        lobbies.append(Lobby(conn, 1, user_info.game_type, len(lobbies)))
        lobby = lobbies[-1]
        lobby.active_turn = turn
        conn.send(pickle.dumps(Response(user_info.game_type, addr=addr, turn=turn, host=True, update=True)))   # send clients turn
        host = True
        server_q_put('Created new lobby:', lobby.id)

    client_id = turn    # set clients id to his turn

    while True:
        if not running:
            conn.send(pickle.dumps(Response(addr=addr, update=True)))
            return
        try:
            data = pickle.loads(conn.recv(PICKLE_SIZE))
            if not data:
                break
            elif data.type['host']['host']:
                if data.type['host']['wait_for_clients']:
                    conn.send(pickle.dumps(Response(user_info.game_type, addr=addr, host=True, clients=[[x['id'], x['role']] for x in lobby.clients])))     # send update to host
                elif len(data.type['host']['ban_clients']) > 0:
                    for ban in data.type['host']['ban_clients']:
                        try:
                            lobby.remove_client(ban)
                        except:
                            pass
            elif data.type['client']['client']:
                if data.type['client']['lobby_wait']:
                    conn.send(pickle.dumps(Response(is_ready=lobby.ready)))    # send update to user
                elif data.type['client']['start_game_req']:     # update server
                    lobby.ready = True    # start lobby
                    lobby.clients_limit = len(lobby.clients)    # cut new joining players
                    for x in range(len(lobby.game.clients)):
                        lobby.game.update_status(x, 'READY')    # start game for all active players
                    print('Lobby', lobby.id, 'is ready')

                if data.end_game_req:
                    for client in lobby.clients:
                        server_q_put('Sending end game request to:', client['conn'].getsockname())
                        response = Response(end_game_req=True, update=True)
                        client['conn'].send(pickle.dumps(response))
                        if client['conn'] == conn:
                            client['end_game'] = True
                elif lobby.ready:
                    if data.turn == lobby.active_turn:
                        if lobby.game.update_move(data.move, data.turn, data.times):
                            server_q_put('client:', data.type['client']['client_addr'],': | turn:', data.turn, '| move:',data.move)
                            turn = data.turn
                            if turn < lobby.game.clients_limit:
                                next_turn = turn+1
                            else:
                                next_turn = 1
                            for client in lobby.clients:
                                if client == 0:
                                    continue
                                try:
                                    lobby.active_turn = next_turn
                                    response = Response(move=data.move, active_turn=lobby.active_turn, update=True)
                                    client['conn'].send(pickle.dumps(response))
                                except ConnectionResetError as e:
                                    if client['role'] == 'HOST' and client['conn'] != conn:
                                        server_q_put('Host closed connection')
                                        conn.send(pickle.dumps(Response(exit_req=True)))    # send msg to player that host has already endet this lobby
                                        break
                                    else:
                                        lobby.active_turn = turn
                                        server_q_put('User:', client['id'], 'went offline', e)
                                        strikes += 1
                                except OSError as e:
                                    lobby.active_turn = turn
                                    server_q_put('User:', client['id'], 'went offline', e)
                                    strikes += 1
                            turn = next_turn
                        else:
                            conn.send(pickle.dumps(Response(addr=addr, change_move_req=True)))   # send invalid move response back to client
                            time.sleep(0.1)   # shadowban not to slow down the server in case of overflow of invalid messages
                            strikes += 1
                    else:
                        server_q_put('turn:', turn, 'got:', data.turn)

                temp = []
                for client in lobby.clients:
                    try:
                        temp.append(client['end_game'])
                    except TypeError:
                        pass
                end_game = all(temp)
                if end_game:
                    server_q_put('Closing lobby:', lobby.id)
                    conn.send(pickle.dumps(Response(exit_req=True)))  # TODO: change this message to summary of the game

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
            server_q_put("Couldn't load data:", e)
        except ConnectionAbortedError as e:
            server_q_put('Client:', addr, 'closed connection', e)
            break
        except ConnectionResetError as e:
            server_q_put('Client:', addr, 'closed connection', e)
            break
        except EOFError as e:
            server_q_put('Client:', addr, 'closed connection', e)
            break

    try:
        server_q_put("Lost connection with client:", user_info.type['client']['client_addr'], lobby.clients[client_id-1]['role'])
    except:
        pass
    if host:
        for client in lobby.clients:
            if client == 0:
                continue
            try:
                client['conn'].send(pickle.dumps(Response(exit_req=True)))    # if host closet lobby remove all clients from lobby
            except ConnectionResetError:    # if it's host or already closed connection then just continue
                pass
            except TypeError:   # if connection is unrelible than just continue
                pass
            except OSError:
                pass
        lobbies.remove(lobby)   # remove lobby when everyone has disconnected
        server_q_put("Closing Lobby:", lobby.id)
    elif lobby.client_count == 1:
        try:
            lobby.client_count -= 1
            lobbies.remove(lobby)
            server_q_put("Closing Lobby:", lobby.id)
        except:
            pass
    else:
        lobby.remove_client(turn)
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

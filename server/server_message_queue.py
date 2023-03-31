import time
import queue

"""
    Simple message queue to not overload the print screen
    server_msg_queue: queue with size of 1 to wait until previous message is printed
    server_q_put: puts message to queue
"""

server_msg_queue = queue.Queue(maxsize=1)

def server_q_put(*args, q: queue.Queue=server_msg_queue, do_print=True):
    """
    :param args: arguments passed to print()
    :param q: queue to put to
    :param do_print: checks if user want's to print imidiatly
    """
    q.put(args)
    if do_print:
        server_q_print(q)

def server_q_print(q: queue.Queue):
    """
    :param q: queue to print msgs from
    :return: prints all from queue
    """
    for _ in range(q.qsize()):
        try:
            time.sleep(0.1)     # sleep for a little to be sure not to overflow the screen
            print(*q.get())
        except KeyboardInterrupt:
            pass

def get_q_size(q: queue.Queue=server_msg_queue):
    return q.qsize()

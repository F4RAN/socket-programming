# first of all import the socket library
import socket
import ast
import threading
from time import sleep
from termcolor import colored

# Thread locks
check_1 = threading.Lock()
check_2 = threading.Lock()

# Global Variables
clients_1 = []
clients_2 = []


def request(c):
    # server listen for client request
    payload = c.recv(1024)
    # Convert String to Dict
    dict_payload = ast.literal_eval(payload.decode())
    if dict_payload['#'] == 1:
        print('First client sent the sentence')
        check_1.acquire() # lock the door :)
        clients_1.append({'#': 1, 'socket': c, 'sentence': dict_payload['payload']})
        check_1.release()

    if dict_payload['#'] == 2:
        print('Second client is ready')
        check_2.acquire()
        clients_2.append({'#': 2, 'socket': c})
        check_2.release()

    # when a pair of clients exists > length of one list is always 1 because of threading lock
    if len(clients_1) > 0 and len(clients_2) > 0:
        check_1.acquire()
        check_2.acquire()
        # FIFO Strategy
        for i in range(min(len(clients_1), len(clients_2))):
            clients_2[i]['socket'].send(clients_1[i]['sentence'].encode())
            print(colored('sentence sent to second client', 'green'))
            result = clients_2[i]['socket'].recv(1024)
            result = result.decode()
            result = ast.literal_eval(result)
            if result['#'] == 'result':
                clients_1[i]['socket'].send(str(result).encode())

            clients_1.pop(0)
            clients_2.pop(0)
        check_2.release()
        check_1.release()
        print('a pair of first and second client released')




def main():
    # reserve a port on your computer in our
    # case it is 3000 but it can be anything
    port = 3000

    # next create a socket object

    s = socket.socket()
    # prevent port in use error
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("Socket successfully created")

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', port))
    print("socket binded to %s" % (port))

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until we interrupt it or
    # an error occurs
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    try:
        while True:
            # receive a connection request
            c, addr = s.accept()
            print("\nconnection received from: ", addr)
            # run functions as a threads
            receive_thread = threading.Thread(target=request, args=[c])
            receive_thread.daemon = True
            receive_thread.start()

    except:
        s.close()



if __name__ == "__main__":
    main()

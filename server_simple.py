# first of all import the socket library
import socket
import ast
from time import sleep

from termcolor import colored

# reserve a port on your computer in our
# case it is 3000 but it can be anything
port = 3000

# next create a socket object
s = socket.socket()
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

"""
this list defined to save client sockets and send correct response to each one.
"""
clients = []
end = False
while True:
    # Establish connection with client.
    c, addr = s.accept()
    print('Got connection from', addr)
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    # server listen for client request
    payload = c.recv(1024)
    # Convert String to Dict
    dict_payload = ast.literal_eval(payload.decode())

    if dict_payload['#'] == 1:
        print('First client sent the sentence')
        sentence = dict_payload['payload']
        clients.append({'#': 1, 'socket': c})

    if dict_payload['#'] == 2:
        print('Second client is ready')
        clients.append({'#': 2, 'socket': c})

    """
    if both clients was ready, send setence to second client
    else if both client was from same source show error, disconnect clients, and show exception
    """
    if len(clients) == 2 and clients[0]['#'] != clients[1]['#']:
        # send setence to second client
        for (index, client) in enumerate(clients):
            if client['#'] == 2:
                client['socket'].send(sentence.encode())
                print(colored('sentence sent to second client', 'green'))
                result = client['socket'].recv(1024)
                result = result.decode()
                result = ast.literal_eval(result)
                if result['#'] == 'result':
                    clients[1 - index]['socket'].send(str(result).encode())  # Complementary of current index
                    end = True
    elif len(clients) == 2 and clients[0]['#'] == clients[1]['#']:
        print(colored('You can not run same clients', 'red'))
        for client in clients:
            client['socket'].close()
        break
    if end:
        break

s.close()
    # c.send('client pub key received successfully'.encode())
    # c.close()

# Breaking once connection closed
#     break

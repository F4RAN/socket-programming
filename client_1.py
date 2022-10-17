# Import socket module
import ast
import socket
from time import sleep
from termcolor import colored

# Create a socket object


s = socket.socket()

# Define the port on which you want to connect
server_port = 3000

# connect to the server on local computer
s.connect(('127.0.0.1', server_port))
packet = str({'#':1, 'payload':'I know Java, Python, JavaScript and Amelia knows C++, Python,& JavaScript'}).encode()
s.send(packet)
sleep(1)


# receive data from the server and decoding to get the string.
while True:
    try:
        reply = s.recv(1024)
        if not reply:
            break

        result = reply.decode()
        result = ast.literal_eval(result)
        print(colored('------------------------'))
        print(colored('Result:','blue'))
        for rep in result['payload']:
            print(colored(f'{rep["word"]} is repeated {rep["repeat"]} times','yellow'))
    except KeyboardInterrupt:
        print('error')

s.close()


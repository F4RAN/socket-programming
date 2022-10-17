# Import socket module
import socket
from time import sleep
from ast import literal_eval

# Create a socket object


s = socket.socket()

# Define the port on which you want to connect
server_port = 3000

# connect to the server on local computer
s.connect(('127.0.0.1', server_port))
packet = str({'#': 2, 'payload': 'ready'}).encode()
s.send(packet)
sleep(1)
repeats_schema = []
# receive data from the server and decoding to get the string.
while True:
    try:
        reply = s.recv(1024)
        if not reply:
            break
        sentence = reply.decode()
        sentence = sentence.replace(',', '')
        sentence = sentence.replace('&', '')
        words = sentence.split(" ")
        for word in set(words):
            repeat = words.count(word)
            if repeat > 1:
                repeats_schema.append({'word':word,'repeat':repeat})
        print('second client is processing sentence...')
        s.send(str({'#': 'result', 'payload': repeats_schema}).encode())
        break

    except KeyboardInterrupt:
        print('error')


s.close()

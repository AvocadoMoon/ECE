import socket
import random
import protocol

IP = "127.0.0.1"    # IP address points to ourself
PORT = 3401        # completely random port number

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
# sock.connect((IP, PORT))    # connect to the server

# while True:
#     msg = sock.recv(1024).decode()    # receive a message from the server
#     print("Server: ", msg)
#     if msg == "q":
#         sock.close()
#         break

#     output = input()
#     sock.send(output.encode()) # send a message to the server
#     if output == "q":
#         sock.close()
#         break


bob = protocol.Client(3401, "127.0.0.1", "Bob")
bob.connect()
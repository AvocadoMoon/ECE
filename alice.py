import socket
import protocol

# Alice is acting as the "server"

IP = "127.0.0.1"    # IP address points to ourself
PORT = 3401         # completely random port number

#AF_INET means IPV4
#SOCK_STREAM means connection-oriented TCP protocol

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
# sock.bind((IP, PORT))   # bind to the specified IP address and port number
# sock.listen(3)          # prepare to listen for incoming connections

# def handleClientConnection(clientsock, addr):
#     while True:
#         output = input()    # get user input from alice
#         clientsock.send(output.encode())    # send a hello message to the client as a byte string
#         if output == "q":   # if alice wants to quit, then quit
#             clientsock.close()
#             break
#         response = clientsock.recv(1024).decode()   # receive a reply from the client and convert it back to a regular string
#         if response == "q":
#             clientsock.close()  # end the socket connection with our client
#             break               # break out of the loop
#         else:
#             print("Client: ", response) 
            

# clientsock, addr = sock.accept()    # accept a connection from a client
# handleClientConnection(clientsock, addr)

alice = protocol.Server(3401, "127.0.0.1", "Alice")

alice.connectClient()


# References;
# https://www.geeksforgeeks.org/socket-programming-python/
# https://realpython.com/python-sockets/ 





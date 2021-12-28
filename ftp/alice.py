import socket

# Alice is acting as the "server"

IP = "127.0.0.1"    # IP address points to ourself
PORT = 3400         # completely random port number

#AF_INET means IPV4
#SOCK_STREAM means connection-oriented TCP protocol

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
sock.bind((IP, PORT))   # bind to the specified IP address and port number
sock.listen(3)          # prepare to listen for incoming connections

# def handleClientConnection(clientsock, bytes):
#     size = str(len(bytes))
#     print(type(size))
#     print(size)
#     clientsock.send(size.encode())  # send the payload size
#     response = clientsock.recv(1024)
#     if response.decode() == "OK":
#         clientsock.send(bytes)  # send the actual data
#     else:   # if bob did not respond with "OK"... alice is going to abort
#         print('Alice is aborting')
#         exit
            
# f = open('kitten.png', 'rb')    # open the image for reading
# bytes = f.read()  # read the bytes 
clientsock, addr = sock.accept()    # accept a connection from a client
#handleClientConnection(clientsock, bytes)   # handle the connection

file = open("kitten.png", "rb")
while True:
    bytes = file.read(1024)
    if len(bytes) == 0:
        break
    clientsock.send(bytes)

file.close()
clientsock.close()
sock.close()
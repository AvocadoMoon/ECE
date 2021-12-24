import socket
import threading

#due to similarity in how client and server recieve messages, just create a class for both
class Transportation():
    def textMessage(self, sock):
        def sendMessage():
            pass

        def recieveMessage():
            pass

    def fileTransfer(self):
        pass

class Client():
    def __init__(self, PORT, IP, name):
        self.IP = IP
        self.PORT = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
        self.name = name
        self.transport = Transportation()
        if (type(self.name) != type(" ")):
            raise TypeError
    
    def connect(self):
        self.sock.connect((self.IP, self.PORT))    # connect to the server
        self.sock.send(self.name.encode())      #in future already have encryption set up and message through that
        response = self.sock.recv(1024).decode()
        if (response == "Y"):
            self.transport.textMessage(self.sock)

    

class Server():
    def __init__(self, PORT, IP, name):
        self.IP = IP
        self.PORT = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
        self.clientSock = None
        self.addr = None
        self.name = name
        self.transport = Transportation()
        if (type(self.name) != type(" ")):
            raise TypeError
    
    def connectClient(self):
        self.sock.bind((self.IP, self.PORT))   # bind to the specified IP address and port number
        self.sock.listen(3)          # prepare to listen for incoming connections
        self.clientsock, self.addr = self.sock.accept()    # accept a connection from a client

        name = self.clientsock.recv(1024).decode()      #no way to authenticate clients name yet
        msg = input("Do you want to communicate with: " + name + "? (Y/N)") #allow more options other than just text based communication in the future
        if (msg == "Y"):
            self.clientSock.send("Y".encode())
            self.transport.textMessage(self.clientSock)
        self.clientSock.send("No".encode())
    


#class all for encyrption and decryption of data, along with other functions that relate to the protocol
class Protocol():
    pass




#IDEAS:
# -- if diffie, send a tupple of keys from both parties in one message
# -- have one thread listening for messages and another for sending messages, that way it won't have to be a call response method for Alice and Bob

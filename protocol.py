import socket
import threading

#due to similarity in how client and server recieve messages, just create a class for both
class Transportation():
    def __init__(self, selfName):
        self.selfName = selfName
        self.othersName = None

    def textMessage(self, sock):
        def sendMessage(sock, selfName):
            while True:
                output = input()
                if output == "q":
                    sock.send((selfName + " Has Left").encode())
                    break
                sock.send(output.encode())


        def recieveMessage(sock, othersName):
            while True:
                msg = sock.recv(1024).decode()
                if (msg == "q"):
                    break
                print(othersName + ": " + msg)
    
        send = threading.Thread(target=sendMessage, args=(sock, self.selfName))
        recieve = threading.Thread(target=recieveMessage, args=(sock, self.othersName, ))

        send.start()
        recieve.start()

        recieve.join()
        send.join

        sock.close()
    

    def fileTransfer(self, sock):
        def sendFile(self, sock):
            pass

        def recieveFile(self, sock):
            pass

class Client():
    def __init__(self, PORT, IP, name):
        self.IP = IP
        self.PORT = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
        self.name = name
        self.transport = Transportation(name)
        if (type(self.name) != type(" ")):
            raise TypeError
    
    def connect(self):
        self.sock.connect((self.IP, self.PORT))    # connect to the server
        self.sock.send(self.name.encode())      #in future already have encryption set up and message through that
        response = self.sock.recv(1024).decode()
        if (response == "Y"):
            serverName = self.sock.recv(1024).decode()
            self.transport.othersName = serverName
            self.transport.textMessage(self.sock)

    

class Server():
    def __init__(self, PORT, IP, name):
        self.IP = IP
        self.PORT = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
        self.name = name
        self.transport = Transportation(name)
        if (type(self.name) != type(" ")):
            raise TypeError
    
    def connectClient(self):
        self.sock.bind((self.IP, self.PORT))   # bind to the specified IP address and port number
        self.sock.listen(3)          # prepare to listen for incoming connections
        clientSock, addr = self.sock.accept()    # accept a connection from a client

        name = clientSock.recv(1024).decode()      #no way to authenticate clients name yet
        self.transport.othersName = name
        msg = input("Do you want to communicate with: " + name + "? (Y/N) ") #allow more options other than just text based communication in the future
        if (msg == "Y"):
            clientSock.send("Y".encode())
            clientSock.send(self.name.encode())
            self.transport.textMessage(clientSock)
        clientSock.send("No".encode())
    


#class all for encyrption and decryption of data, along with other functions that relate to the protocol
class Protocol():
    pass




#IDEAS:
# -- if diffie, send a tupple of keys from both parties in one message
# -- have one thread listening for messages and another for sending messages, that way it won't have to be a call response method for Alice and Bob

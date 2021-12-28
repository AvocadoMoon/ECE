import socket
import threading

#due to similarity in how client and server recieve messages, just create a class for both
class Transportation():
    def __init__(self, selfName, serverSock=None):
        self.selfName = selfName
        self.stop = False
        self.serverSock = serverSock

    def textMessage(self, sock):
        def sendMessage(self, sock, selfName):
            while True:
                # start mutex
                output = input()
                # end mutex
                if output == "q" or self.stop:
                    sock.send((selfName + " Has Left").encode())
                    self.stop = True
                    break
                sock.send((selfName + ": " + output).encode())


        def recieveMessage(self, sock):
            while True:
                # start mutex
                msg = sock.recv(1024).decode()
                # end mutex
                if (msg == "q") or self.stop:
                    print(msg)
                    print("Disconnected Bye")
                    self.stop = True
                    break
                print(msg)
    
        send = threading.Thread(target=sendMessage, args=(self, sock, self.selfName))
        recieve = threading.Thread(target=recieveMessage, args=(self, sock, ))

        send.start()
        recieve.start()

        recieve.join()
        send.join()

        sock.close()

        if not(self.serverSock):
            self.serverSock.close()
    

    def fileTransfer(self, sock):
        def sendFile(self, sock):
            pass

        def recieveFile(self, sock):
            pass


#need to put in an error catch for when server is not there
class Client():
    def __init__(self, PORT, IP, name):
        self.__IP__ = IP
        self.__PORT__ = PORT
        self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
        self.__name__ = name
        self.__transport__ = Transportation(name)
        if (type(self.__name__) != type(" ")):
            raise TypeError
    
    def connect(self):
        self.__sock__.connect((self.__IP__, self.__PORT__))    # connect to the server
        self.__sock__.send(self.__name__.encode())      #in future already have encryption set up and message through that

        response = self.__sock__.recv(1024).decode()
        if (response == "Y"):
            self.__transport__.textMessage(self.__sock__)   # starts two threads
        else:
            self.__sock__.close()
    

class Server():
    def __init__(self, PORT, IP, name):
        self.__IP__ = IP
        self.__PORT__ = PORT
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
        self.__sock__ = sock
        self.__name__ = name
        self.__transport__ = Transportation(name, sock)
        if (type(self.__name__) != type(" ")):
            raise TypeError
    
    def connectClient(self):
        self.__sock__.bind((self.__IP__, self.__PORT__))   # bind to the specified IP address and port number
        self.__sock__.listen(3)          # prepare to listen for incoming connections
        clientSock, addr = self.__sock__.accept()    # accept a connection from a client

        name = clientSock.recv(1024).decode()      #no way to authenticate clients name yet

        msg = input("Do you want to communicate with: " + name + "? (Y/N) ") #allow more options other than just text based communication in the future
        if (msg == "Y"):
            clientSock.send("Y".encode())
            self.__transport__.textMessage(clientSock)  # starts two threads
        else:
            clientSock.send("No".encode())
            clientSock.close()


#class all for encyrption and decryption of data, along with other functions that relate to the protocol
class Protocol():
    pass




#IDEAS:
# -- if diffie, send a tupple of keys from both parties in one message
# -- have one thread listening for messages and another for sending messages, that way it won't have to be a call response method for Alice and Bob

import socket
import threading
import copy

#due to similarity in how client and server recieve messages, just create a class for both
class Transportation():
    def __init__(self, selfName, serverSock=None):
        self.selfName = selfName
        self.stop = False
        self.serverSock = serverSock
        self.fileCommand = "file \n"    #the newline at the end can not be sent through regular messages due to strip, signify file is being sent
        self.specialCharsDict = {ord('\n'): 'newline', ord('\t'): 'tab'} #ord makes ASCII number out of char

    def textMessage(self, sock):
        def sendMessage(self, sock):
            while True:
                # start mutex
                output = input()
                output = self.sanatize(output)        #need to sanatize so that certain characters are limited and therefore can be used to signal certain functions, don't want user to be able to acess through typing string
                # end mutex
                if output == "q" or self.stop:
                    sock.send((self.selfName + " Has Left").encode())
                    sock.send("q".encode())
                    self.stop = True
                    break


                elif output == "-h":
                    string = "Help: \n -h: Brings the help table \n -f: Goes into file transportation mode \n"
                    print(string)
                
                #send intent of file transfer, send filename, get response, send file or go back to message mode
                elif output == "-f":
                    sock.send(self.fileCommand.encode())
                    output = input("Please give the files path: ")
                    fileName = output.split('\\')[-1]
                    sock.send(fileName.encode())
                    print("Waiting for reciever to accept file.")
                    msg = sock.recv(1024).decode()
                    if msg == "Y":
                        print("Output: " + output)
                        self.sendFile(sock, output)
                    else:
                        print("They rejected the file transfer")
                else:
                    sock.send((self.selfName + ": " + output).encode())


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


                elif msg == self.fileCommand:
                    fileName = sock.recv(1024).decode()
                    output = input("Would you want to recieve the file '" + fileName + "'? (Y/N): ")
                    if output == "Y":
                        sock.send("Y".encode())
                        output = input("Where would you want to save the file? (Path): ")
                        self.recieveFile(sock, output)
                    else:
                        print("File transfer not executed")

                
                else:
                    print(msg)
    
        send = threading.Thread(target=sendMessage, args=(self, sock))
        recieve = threading.Thread(target=recieveMessage, args=(self, sock, ))

        send.start()
        recieve.start()

        recieve.join()
        send.join()

        sock.close()

        if self.serverSock != None:
            self.serverSock.close()
    

    
    def sendFile(self, sock, filePath):
        file = open(filePath, "rb")
        while True:
            bytes = file.read(1024)
            if len(bytes) == 0:
                break
            sock.send(bytes)
        file.close()

    def recieveFile(self, sock, savePath):
        file = open(savePath, "wb")
        while True:
            data = sock.recv(1024)
            file.write(data)
            if len(data) != 1024:
                break
        file.close()
    
    def sanatize(self, msg):
        msg.translate(self.specialCharsDict) #changes all chars in msg to accaptable messages specified in the dict, key entry is replaced by value entry
        return msg


#need to put in an error catch for when server is not there
class Client():
    def __init__(self, PORT, IP, name):
        self.__IP__ = IP
        self.__PORT__ = PORT
        self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
        self.__name__ = name.strip()
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


#class all for encyrption and decryption of data
class Encryption():
    pass




#IDEAS:
# -- if diffie, send a tupple of keys from both parties in one message
# -- have one thread listening for messages and another for sending messages, that way it won't have to be a call response method for Alice and Bob
# -- private class filled with command strings where the user can't access it

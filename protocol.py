import socket
import threading
import copy
import os
import time

#due to similarity in how client and server recieve messages, just create a class for both
class Transportation():
    def __init__(self, selfName, serverSock=None):
        self.selfName = selfName
        self.stop = False
        self.serverSock = serverSock
        self.fileCommand = "file \n"    #the newline at the end can not be sent through regular messages due to strip, signify file is being sent
        self.specialCharsDict = {ord('\n'): 'newline', ord('\t'): 'tab'} #ord makes ASCII number out of char

    def textMessage(self, sock):
        def sendMessage(self, sock, stop, inputLock):
            while True:
                time.sleep(1)
                output = input()
                output = self.sanatize(output)        #need to sanatize so that certain characters are limited and therefore can be used to signal certain functions, don't want user to be able to acess through typing string
                if output == "q" or stop.is_set():
                    sock.send((self.selfName + " Has Left").encode())
                    sock.send("q".encode())
                    self.stop = True
                    break


                elif output == "-h":
                    string = "Help: \n -h: Brings the help table \n -f: Goes into file transportation mode \n"
                    print(string)
                

                elif output == "-f":
                    sock.send(self.fileCommand.encode())    #send intent of file transfer

                    output = input("Please give the files path: ")  #get file name and send it
                    # fileName = output.split('\\')[-1]
                    # sock.send(fileName.encode())

                    self.sendFile(sock, output)     #send file

                    # print("Waiting for reciever to accept file.")   #get response
                    # msg = sock.recv(1024).decode()
                    # if msg == "Y":
                    #     self.sendFile(sock, output)     #send file
                    # else:
                    #     print("They rejected the file transfer")    #say file gets rejected
                else:
                    sock.send((self.selfName + ": " + output).encode())


        def recieveMessage(self, sock, stop, inputLock):
            while True:
                msg = sock.recv(1024).decode()
                if (msg == "q") or self.stop:
                    print(msg)
                    print("Disconnected Bye")
                    self.stop = True
                    break

                
                #cant use input functions since in other thread for send, its input has control over Erno, need to create some other input probabliy through GUI
                elif msg == self.fileCommand:   #check intent of file transfer
                    # fileName = sock.recv(1024).decode()     #get file name
                    # input("Would you want to recieve the file '" + "" + "'? (Y/N): ")    #accept or decline file
                    # sock.send(output.encode())  #send response
                    # if output == "Y":
                    #     output = input("Where would you want to save the file? (Path): ")   #specify where to save it
                    #     self.recieveFile(sock, output)  #recieve file
                    # else:
                    #     print("File transfer not executed")
                    self.recieveFile(sock, "t")

                
                else:
                    print(msg)
    
        stop = threading.Event()
        inputLock = threading.Lock()
        recieve = threading.Thread(target=recieveMessage, args=(self, sock, stop))
        send = threading.Thread(target=sendMessage, args=(self, sock, stop))


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
class Connection():
    def __init__(self, PORT, IP, name, server):
        self.__IP__ = IP
        self.__PORT__ = PORT
        self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
        self.__name__ = name.strip()
        self.__transport__ = Transportation(name)
        self.__server__= server
        self.__communicationSockets__ = []
        self.fileCommand = "file \n"    #the newline at the end can not be sent through regular messages due to strip, signify file is being sent
        self.specialCharsDict = {ord('\n'): 'newline', ord('\t'): 'tab'} #ord makes ASCII number out of char
        if (type(self.__name__) != type(" ")):
            raise TypeError
    
    def connect(self):
        if self.__server__:
            self.__sock__.bind((self.__IP__, self.__PORT__))   # bind to the specified IP address and port number
            self.__sock__.listen(3)          # prepare to listen for incoming connections
            clientSock, addr = self.__sock__.accept()    # accept a connection from a client
            self.__communicationSockets__.append(clientSock)
        else:  
            self.__sock__.connect((self.__IP__, self.__PORT__))    # connect to the server
            self.__communicationSockets__.append(self.__sock__)    # make the socket be a communication socket

    def sendMessage(self, msg):
        msg = self.sanatize(msg)
        msg = self.__name__ + ": " + msg
        for i in self.__communicationSockets__:
            i.send(msg.encode())

    def recieveMessage(self):
        for i in self.__communicationSockets__:
            msg = i.recv(1024).decode()
        return msg

    def sendFile(self, filePath):
        for i in self.__communicationSockets__:
            file = open(filePath, "rb")
            while True:
                bytes = file.read(1024)
                if len(bytes) == 0:
                    break
                i.send(bytes)
            file.close()
    
    def recieveFile(self, savePath):
        for i in self.__communicationSockets__:
            file = open(savePath, "wb")
            while True:
                data = i.recv(1024)
                file.write(data)
                if len(data) != 1024:
                    break
            file.close()
    
    def sanatize(self, msg):
        msg.translate(self.specialCharsDict) #changes all chars in msg to accaptable messages specified in the dict, key entry is replaced by value entry
        return msg
    
    def disconnect(self):
        pass

    def userJoined(self):
        pass

#class all for encyrption and decryption of data
class Encryption():
    pass




#IDEAS:
# -- if diffie, send a tupple of keys from both parties in one message
# -- have one thread listening for messages and another for sending messages, that way it won't have to be a call response method for Alice and Bob
# -- private class filled with command strings where the user can't access it
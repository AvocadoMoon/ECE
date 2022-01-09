import socket
import threading
import copy
import os
import time


#need to put in an error catch for when server is not there
class Connection():
    def __init__(self, PORT, IP, name, server, gui):
        self.__IP__ = IP
        self.__PORT__ = PORT
        self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
        self.__name__ = name.strip()
        self.__server__= server
        self.guiPointer = gui
        self.__communicationSockets__ = []
        self.__communicationThreads = []
        self.fileCommand = "file \n"    #the newline at the end can not be sent through regular messages due to strip, signify file is being sent
        self.specialCharsDict = {ord('\n'): 'newline', ord('\t'): 'tab'} #ord makes ASCII number out of char
        self.__communicationLock = threading.Lock()
        if (type(self.__name__) != type(" ")):
            raise TypeError
    
    def _serverConnect(self):
        while True:
                clientSock, addr = self.__sock__.accept()    # accept a connection from a client
                self.__communicationLock.acquire() # make sure that when accesing list which is called out of thread, that thread is not messing with it, lock
                self.__communicationSockets__.append(clientSock)
                thread = threading.Thread(target=self.recieveMessage, args=[clientSock])
                thread.start()
                self.__communicationThreads.append(thread)
                self.__communicationLock.release() # unlock


    def connect(self):
        if self.__server__:
            self.__sock__.bind((self.__IP__, self.__PORT__))   # bind to the specified IP address and port number
            self.__sock__.listen(3)          # prepare to listen for incoming connections, 3 is the number of connections that will be put on hold while server is busy
            self.__serverConnectionThread = threading.Thread(target=self._serverConnect)
            self.__serverConnectionThread.start()
        else:
            thread = threading.Thread(target=self.recieveMessage)
            self.__communicationThreads.append(thread)
            self.__sock__.connect((self.__IP__, self.__PORT__))    # connect to the server
            thread.start()

    def sendMessage(self, msg):
        msg = self.sanatize(msg)
        msg = self.__name__ + ": " + msg

        #send message to all clients that are currently connected, server is the only object which has the info of every person
        if self.__server__:
            self.__communicationLock.acquire() #lock
            for i in self.__communicationSockets__:
                i.send(msg.encode())
            self.__communicationLock.release() #unlock
        
        #client sends message to server, then server relays it to all clients
        else:
            self.__sock__.send(msg.encode())

    # recieve message and return it to be displayed
    def recieveMessage(self, sock=None):
        while True:
            msg = ""
            if self.__server__: #non server just needs to recieve message
                msg = sock.recv(1024).decode()
                self._serverRelayMessage(sock, msg)
            if not(self.__server__):    #server is responsible for all handling of information so when a client sends a message it needs to relay its message to all other clients
                msg = self.__sock__.recv(1024).decode()
            self.guiPointer.displayRecievedMessages(msg)
    
    # server handles all information sending
    def _serverRelayMessage(self, sock, msg):
        self.__communicationLock.acquire() #lock
        for i in self.__communicationSockets__: #relay message to all clients except for the one who sent it
            if i == sock:
                pass
            else:
                i.send(msg.encode())
        self.__communicationLock.release() #unlock

    #TO DO: implement send file
    def sendFile(self, filePath):
        self.__communicationLock.acquire() #lock
        for i in self.__communicationSockets__:
            file = open(filePath, "rb")
            while True:
                bytes = file.read(1024)
                if len(bytes) == 0:
                    break
                i.send(bytes)
            file.close()
        self.__communicationLock.release() #unlock
    
    def recieveFile(self, savePath):
        self.__communicationLock.acquire() #lock
        for i in self.__communicationSockets__:
            file = open(savePath, "wb")
            while True:
                data = i.recv(1024)
                file.write(data)
                if len(data) != 1024:
                    break
            file.close()
        self.__communicationLock.release() #unlock
    
    def sanatize(self, msg):
        msg.translate(self.specialCharsDict) #changes all chars in msg to accaptable messages specified in the dict, key entry is replaced by value entry
        return msg
    
    #TO DO
    #clean up all open files or such
    def disconnect(self):
        self.__communicationLock.acquire() #lock

        #by closing the sockets it will cause errors in the threads using them, then this will hopefully cause the threads to terminate and easly join, TO DO test this
        self.__sock__.close()
        for i in self.__communicationSockets__:
            i.close()
        for i in self.__communicationThreads:
            i.join()
        
        self.__communicationLock.release()  #unlock, but its not like anything else will use it after its all been closed
#class all for encyrption and decryption of data
class Encryption():
    pass




#IDEAS:
# -- if diffie, send a tupple of keys from both parties in one message
# -- have one thread listening for messages and another for sending messages, that way it won't have to be a call response method for Alice and Bob
# -- private class filled with command strings where the user can't access it
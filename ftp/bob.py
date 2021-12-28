import socket
import random
import PIL.Image as Image
from PIL import ImageFile
import io

IP = "127.0.0.1"    # IP address points to ourself
PORT = 3400         # completely random port number
ImageFile.LOAD_TRUNCATED_IMAGES = True  # credit to: https://stackoverflow.com/questions/12984426/pil-ioerror-image-file-truncated-with-big-images 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket object, uses a TCP connection
sock.connect((IP, PORT))    # connect to the server

# file_size = sock.recv(10000000) # receive the payload size (aka how many bytes the image will be)
# print(file_size)
# sock.send(b'OK')
# file_size = int(file_size.decode())
# msg = sock.recv(file_size)    # receive a message from the server
# img = Image.open(io.BytesIO(msg)) # load the image as a byte stream?
# # img.show() # simply display the image
# img.save("bob_received.png", "PNG")  # save the image we received as a new file

file = open("file.png", "wb")
while True:
    data = sock.recv(1024)
    file.write(data)
    if len(data) != 1024:
        break
file.close()
sock.close()

# miscellaneous: receive bytes incrementally...
''' remaining = file_size    # remaining number of bytes that bob needs to receive
received = ''

while remaining != 0:   # while there are still bytes to be received...
    msg = sock.recv(remaining).decode()    # receive a message from the server
    received += msg     # concatenate
    remaining -= len(msg)   # update how many bytes are remaining
'''
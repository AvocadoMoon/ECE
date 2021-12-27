ok so here's how it works and how to DIY

how it works: 
    alice.py
        - creates a socket, binds, listens
        - opens the kitten.png image and reads the bytes 
        - accepts a connection from bob
        - find out how many bytes the image contains and sends that number to bob 
        - receive bob's response (hopefully, "OK")
        - send the actual bytes of the image to bob (or abort if bob can't handle it)

    bob.py 
        - create a socket, connect to alice 
        - receive the number of bytes 
        - send OK 
        - receive the actual bytes of the image 
        - create an Image object with those bytes ^
        - save the image as "bob_received.png"


how to DIY: 
- open a split terminal
- in one terminal, run alice.py 
- in the other terminal, run bob.py 
- let the magic happen (i.e., you will see a new file appear called "bob_received.png". open it!)
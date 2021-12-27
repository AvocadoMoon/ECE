import PIL.Image as Image
import io

# use PIL library to simply open an image, read the bytes of the image, and then show the image!

f = open('kitten.png', 'rb')    # open the image for reading
bytes = f.read()  # read the bytes 
img = Image.open(io.BytesIO(bytes)) # create an image object
img.show()  # actually display the image

# this works!
# credit to: https://youtu.be/xZF6zWLz-vY 


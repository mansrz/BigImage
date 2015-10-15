'''
Proyecto de Procesamiento Digital de Imagenes

Base de datos de imagen

Pasa el mouse por la imagen que contiene todas las imagenes
presentar un popup de la imagen y si se le da clikc mostrarla
para poder guardar o revisarla

##bibligrafia
http://opencv-srf.blogspot.com/2011/11/mouse-events.html


'''

import cv2
from cv2 import cv
import numpy as np
import csv

'''
ALGORITMO


1 leer un archivo separados por comas que contengan nombre de imagenes
2 crear imagefull de tamano segun el numero de imagenes cargadas
3 cada imagen reducirla de tamano
4 agregar imagen reducida a imagenfull
5 guardar posiciones
6 crear objeto con el nombre de imagen y posicion
6 repetir 3 hasta completar todas las imagenes
7 agregar evento de mouseover con la funcion para mostrar la imagen
8 agregar evento de click con la funcion para obtener la imagen


'''


files = []
#Read file
with open('ls.txt', 'r') as file:
    for line in file:
        files.append(line.split('\n')[0])
num = len(files)/6

#Define Class Small Image

class SmallImage():
    x = 0
    y = 0
    size = 0
    height = 0
    width = 0
    name = ''

    def __init__(self, x, y, name, size):
        self.x = x
        self.y = y
        self.size = size
        self.height = x + size
        self.width = y + size
        self.name = name

    def isinmyself(self, x, y):
        if(((self.height > x)and(self.x < x))and((self.width > y)and(self.y < y))):
            return True
        return False

    def __str__(self):
        return self.name + ' x:'+self.x+ ' y'+self.y

#Function to create Image
def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)
    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color
    return image

# Function to get Size
def getSize(num):
    return 700/num

# Variables
posx = 0
posy = 0
images = []
size = getSize(num)

# Create new blank 1000x1000 image
# width, height
image = create_blank((num+2)*size, (num-2)*size)

#Merge images
for i in range(num+2):
    for j in range(num-2):
        tb_l = cv2.imread(files[(i*4)+j])
        #Create Object
        small = SmallImage(posy,posx,files[(i*4)+j] ,size)
        #Append Object
        images.append(small)
        #Resize image
        tb_x = cv2.resize(tb_l,(size,size))
        #Add to bigimage
        image[posx:posx+size,posy:posy+size] = tb_x
        posx = posx +size
    posy = posy + size
    posx = 0

#Save BIGIMAGE
cv2.imwrite('bigimage.jpg', image)


#Function to find image in x,y position and show
def findimage (x, y):
    foundit = None
    for image in images:
        if image.isinmyself(x,y):
            foundit = image
    if foundit is not None:
        tb_l = cv2.imread(foundit.name)
        tb_x = cv2.resize(tb_l,(300,300))
        cv2.moveWindow('overthis',foundit.y,foundit.x)
        cv2.imshow('overthis',tb_x)
    else:
        cv2.destroyWindow('overthis')

def mousevent(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for image in images:
                if image.isinmyself(x,y):
                    foundit = image
            if foundit is not None:
                tb_l = cv2.imread(foundit.name)
                tb_x = cv2.resize(tb_l,(500,500))
                cv2.moveWindow('clickthis',0,0)
                cv2.imshow('clickthis',tb_x)

        elif event == cv2.EVENT_MOUSEMOVE:
            findimage(x,y)

#Read image to load and show
image = cv2.imread('bigimage.jpg')
clone = image.copy()
cv2.namedWindow("image")
#Add Mouse event function
cv2.setMouseCallback("image", mousevent)

# keep looping until the 'q' key is pressed
while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
                image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
                break



import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import *

from Functions_splitted import Gera_Contornos
from Functions_splitted import Gera_Lista_Pontos_Contorno

img_in = cv2.imread("imgs_iniciais/novapizza.webp", cv2.IMREAD_COLOR)

contours = Gera_Contornos(img_in)

pontos = Gera_Lista_Pontos_Contorno(img_in,contours)
print (pontos)


import cv2

def resize_with_aspect_ratio(image, tamanho_folha):
    current_height, current_width = image.shape[:2]
    width = tamanho_folha[0]
    height = tamanho_folha[1]

    if height>width:
        width = 0
    
    if width>height:
        height = 0

    if width == 0:
        # Calculate the ratio based on the desired height
        ratio = height / float(current_height)
        new_width = int(current_width * ratio)
        new_height = height
    else:
        # Calculate the ratio based on the desired width
        ratio = width / float(current_width)
        new_width = width
        new_height = int(current_height * ratio)
    
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

# Load the image
image = cv2.imread('input_image.jpg')

# Resize the image while maintaining aspect ratio
resized_image = resize_with_aspect_ratio(image, width=500)  # Set the desired width

# Display the resized image
cv2.imshow('Resized Image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
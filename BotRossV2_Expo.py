#PT_BR bibliotecas para processamento de imagem
#US_EN libraries for image processing

import cv2
import matplotlib.pyplot as plt
import numpy as np
from pykuwahara import kuwahara
from math import *

#PT_BR arquivo criado pelos desenvolvedores para armazenar as funções e deixar o código mais limpo
#US_EN developer created file in order to store the functions and make a cleaner code here
import FunctionsV2

#PT_BR bibliotecas para comunicação com o UR5
#US_EN libraries for UR5 communication
import socket
import time
import threading

# Constants
HOST = '10.103.16.140'  # Replace with the actual IP address of your UR5 robot
PORT_SEND = 12345    # Replace with the desired port for sending data to the robot
PORT_RECEIVE = 12346 # Replace with the desired port for receiving data from the robot

### Code
img_in = cv2.imread(FunctionsV2.select_image(), cv2.IMREAD_COLOR)
#img_in = cv2.imread("imgs_avancadas\PatBenatar.jpg", cv2.IMREAD_COLOR)
if img_in is None:
    print("File not found. Bye!")
    exit(0)

A4_retrato = (297,210) #dimensões em mm (height, width)
A4_paisagem = (210,297) #dimensões em mm (height, width)

resized_image = FunctionsV2.resize_keeping_aspect_ratio(img_in,A4_retrato)

#imagem que o robô irá desenhar:
#img_v = cv2.flip(hsv_img_in_norm, 0) # flip the image by vertically
#img_h = cv2.flip(hsv_img_in_norm, 1) # flip the image by horizontally
#img_in_norm_vh = cv2.flip(hsv_resized_image,-1) # flip the image in both axis

#cores + preto e branco
listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],
                           [60,100,100],[137,85.5,43.1],[197,70,83.5],
                           [214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25],
                           [0,0,10]]

#lista reduzida para testes (cores quentes)
#listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100]]

#lista reduzida para testes (cores frias)
#listaHSV_Cores_Canetas =  [[0,0,100],[197,70,83.5],[214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25]]

simplified_colors = FunctionsV2.Simplify_Image_Colors(resized_image,listaHSV_Cores_Canetas)
simplified_colors_RGB = cv2.cvtColor(simplified_colors, cv2.COLOR_HSV2BGR)

# Display the image with simplified colours
cv2.imshow('cores_finais', simplified_colors_RGB)
cv2.waitKey(0)
cv2.destroyAllWindows()

dict_filings_by_color = FunctionsV2.Split_Colors(simplified_colors, listaHSV_Cores_Canetas)
dict_point_positions_by_color = {}
for element in dict_filings_by_color.keys():
    RGB_split_preview = cv2.cvtColor(dict_filings_by_color[element], cv2.COLOR_HSV2BGR)
    cv2.imshow(element, RGB_split_preview)
    cv2.waitKey(0)
    
    binirized_color =  cv2.cvtColor(dict_filings_by_color[element], cv2.COLOR_BGR2GRAY)
    returns, thresh = cv2.threshold(binirized_color, 1, 255, cv2.THRESH_BINARY)
    point_positions = FunctionsV2.Generate_fillings(thresh, element)

print ('Program Started')
print('Trying Connection')
count = 0
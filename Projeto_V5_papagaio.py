import cv2
import matplotlib.pyplot as plt

import numpy as np
from math import *
import FunctionsV2

img_in = cv2.imread(FunctionsV2.select_image(), cv2.IMREAD_COLOR)
if img_in is None:
    print("File not found. Bye!")
    exit(0)

# Display the image as is imported
cv2.imshow('hsv', img_in)
cv2.waitKey(0)
cv2.destroyAllWindows()

A4_retrato = (297,210) #dimensões em mm (height, width)
A4_paisagem = (210,297) #dimensões em mm (height, width)

resized_image = FunctionsV2.resize_keeping_aspect_ratio(img_in,A4_retrato)
cv2.imshow('Resized Image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#imagem que o robô irá desenhar:
#img_v = cv2.flip(hsv_img_in_norm, 0) # flip the image by vertically
#img_h = cv2.flip(hsv_img_in_norm, 1) # flip the image by horizontally
#img_in_norm_vh = cv2.flip(hsv_resized_image,-1) # flip the image in both axis


#fornecer cores de canetas no formato (H[0-360], S([0-100], V[0-100])
#sem preto, nem branco
#listaHSV_Cores_Canetas =  [[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 48.2],[326, 71.9, 57.3],[0,0,0]]
#cores + preto e branco
#listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25]]

#lista reduzida para testes
listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100]]

hsv_img_out = FunctionsV2.Simplify_Image_Colors(resized_image,listaHSV_Cores_Canetas)
simplified_colors = cv2.cvtColor(hsv_img_out, cv2.COLOR_HSV2BGR)

# Display the image with simplified colours
cv2.imshow('cores_finais', simplified_colors)
cv2.waitKey(0)

#print((img_out[0,0]))
(height,width) = (simplified_colors.shape[0], simplified_colors.shape[1])
img_out = simplified_colors
for color in listaHSV_Cores_Canetas:
    for i in range(height-1):
        for j in range(width-1):
            #print(hsv_img_out[i,j], "o", color)
            if np.all(hsv_img_out[i,j] == color):
                img_out[i,j] =  color
            else:
                img_out[i,j] = [0,0,0]

    img_out = cv2.cvtColor(img_out, cv2.COLOR_HSV2BGR)
    grayscale_colors =  cv2.cvtColor(img_out, cv2.COLOR_BGR2GRAY)
    returns, thresh = cv2.threshold(grayscale_colors, 1, 255, cv2.THRESH_BINARY)

    #cv2.imshow(str(color), img_out)
    #cv2.waitKey(0)

    FunctionsV2.Gera_preenchimento_Vf(thresh)
    #cv2.imshow(str(color), thresh)
    cv2.waitKey(0)
    

#dictionary contining one binary image for each available color
#impossible to store image on dict (unhashable type: "list")
dict_splited_colors = FunctionsV2.Split_Colors(simplified_colors,listaHSV_Cores_Canetas) 

# Display the image with contours
#cv2.imshow('cores_finais', simplified_colors)
#cv2.waitKey(0)
#cv2.destroyAllWindows()    

cv2.destroyAllWindows()
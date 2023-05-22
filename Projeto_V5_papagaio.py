import cv2
import matplotlib.pyplot as plt

import numpy as np
from math import *
import Functions

#img_in = cv2.imread("imgs_avancadas/Imagem1.png", cv2.IMREAD_COLOR)
img_in = cv2.imread("imgs_avancadas/birb.jpeg", cv2.IMREAD_COLOR)
#img_in = cv2.imread("imgs_avancadas\Lenna.png", cv2.IMREAD_COLOR)
if img_in is None:
    print("File not found. Bye!")
    exit(0)



gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
# Apply binary thresholding
_, imagem_binarizada = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
#point_positions = Functions.Gera_preenchimento_V2(imagem_binarizada,10,8)

# Display the image with contours
cv2.imshow('hsv', img_in)
cv2.waitKey(0)
cv2.destroyAllWindows()

#For HSV, hue range is [0,179], saturation range is [0,255], and value range is [0,255]

A4_retrato = (297,210) #dimensões em mm (height, width)
A4_paisagem = (210,297) #dimensões em mm (height, width)

resized_image = Functions.resize_keeping_aspect_ratio(img_in,A4_paisagem)
cv2.imshow('Resized Image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

hsv_resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

[H,S,V] = cv2.split(hsv_resized_image)
(height,width) = H.shape


#imagem que o robô irá desenhar:
#img_v = cv2.flip(hsv_img_in_norm, 0) # flip the image by vertically
#img_h = cv2.flip(hsv_img_in_norm, 1) # flip the image by horizontally
img_in_norm_vh = cv2.flip(hsv_resized_image,-1) # flip the image in both axis


#fornecer cores de canetas no formato (H[0-360], S([0-100], V[0-100])
#listaHSV_Cores_Canetas =  [[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 48.2],[326, 71.9, 57.3],[0,0,0]]
listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25]]
for cor in listaHSV_Cores_Canetas:
    cor[0] = int(np.clip((cor[0])/2,0,255))
    cor[1] = int(np.clip((cor[1]*255)/100,0,255))
    cor[2] = int(np.clip((cor[2]*255)/100,0,255))
#print (listaHSV_Cores_Canetas)

H_out = np.zeros((height,width), dtype = "uint8")
f1 = 1 #peso do h
S_out = np.zeros((height,width), dtype = "uint8")
f2 = 1 #peso do s
V_out = np.zeros((height,width), dtype = "uint8")
f3 = 1 #peso do v

for i in range(height-1):
    for j in range(width-1):
        vci = [H[i,j],S[i,j],V[i,j]] #vetor cor imagem
        lista_dist_eclidiana = []
        for vcc in listaHSV_Cores_Canetas: #vcc = vetor cor canetas

            dist_euclidiana = sqrt(((vcc[0]-vci[0])**2)*f1 + ((vcc[1]-vci[1])**2)*f2 + ((vcc[2]-vci[2])**2)*f3)
            lista_dist_eclidiana.append(dist_euclidiana)

        min_dist_index = np.argmin(lista_dist_eclidiana)
        H_out[i,j] = listaHSV_Cores_Canetas[min_dist_index][0]
        S_out[i,j] = listaHSV_Cores_Canetas[min_dist_index][1]
        V_out[i,j] = listaHSV_Cores_Canetas[min_dist_index][2]
        #print(i,j)

hsv_img_out = cv2.merge((H_out,S_out,V_out))

#img_out = hsv_img_out
img_out = cv2.cvtColor(hsv_img_out, cv2.COLOR_HSV2BGR)

# Display the image with contours
cv2.imshow('cores_finais', img_out)
cv2.waitKey(0)
#cv2.destroyAllWindows()

#print((img_out[0,0]))

for color in listaHSV_Cores_Canetas:

    for i in range(height-1):
        for j in range(width-1):
            #print(hsv_img_out[i,j], "o", color)
            if np.all(hsv_img_out[i,j] == color):
                img_out[i,j] =  color
            else:
                img_out[i,j] = [0,0,0]

    img_out = cv2.cvtColor(img_out, cv2.COLOR_HSV2BGR)
    gray2 =  cv2.cvtColor(img_out, cv2.COLOR_BGR2GRAY)
    returns, thresh = cv2.threshold(gray2, 1, 255, cv2.THRESH_BINARY)

    Functions.Gera_preenchimento_V2(thresh)
    cv2.imshow(str(color), thresh)
    cv2.waitKey(0)
cv2.destroyAllWindows()
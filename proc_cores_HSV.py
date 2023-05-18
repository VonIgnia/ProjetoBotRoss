import cv2
import matplotlib.pyplot as plt

import numpy as np
from math import *

img_in = cv2.imread("imgs_avancadas\Imagem1.png", cv2.IMREAD_COLOR)
img_in = cv2.imread("imgs_avancadas\Lenna.png", cv2.IMREAD_COLOR)
if img_in is None:
    print("File not found. Bye!")
    exit(0)
cv2.imshow('img original', img_in)
cv2.waitKey(0)
cv2.destroyAllWindows()


hsv_img_in = cv2.cvtColor(img_in, cv2.COLOR_BGR2HSV)

#print (hsv_img_in)
# Display the image with contours
cv2.imshow('hsv', hsv_img_in)
cv2.waitKey(0)
cv2.destroyAllWindows()



listaHSV_Cores_Canetas =  [[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 48.2],[326, 71.9, 57.3],[0,0,0]]
for cor in listaHSV_Cores_Canetas:
    cor[0] = int(np.clip((cor[0])/2,0,255))
    cor[1] = int(np.clip((cor[1]*255)/100,0,255))
    cor[2] = int(np.clip((cor[2]*255)/100,0,255))
#print (listaHSV_Cores_Canetas)

#For HSV, hue range is [0,179], saturation range is [0,255], and value range is [0,255]
[H,S,V] = cv2.split(hsv_img_in)

(height,width) = H.shape 

H_out = np.zeros((height,width), dtype = "uint8")
S_out = np.zeros((height,width), dtype = "uint8")
V_out = np.zeros((height,width), dtype = "uint8")

for i in range(height-1):
    for j in range(width-1):
        vci = [H[i,j],S[i,j],V[i,j]] #vetor cor imagem
        lista_dist_eclidiana = []
        for vcc in listaHSV_Cores_Canetas: #vcc = vetor cor canetas

            dist_euclidiana = sqrt((vcc[0]-vci[0])**2 + (vcc[1]-vci[1])**2 + (vcc[2]-vci[2])**2)
            lista_dist_eclidiana.append(dist_euclidiana)

        min_dist_index = np.argmin(lista_dist_eclidiana)
        H_out[i,j] = listaHSV_Cores_Canetas[min_dist_index][0]
        S_out[i,j] = listaHSV_Cores_Canetas[min_dist_index][1]
        V_out[i,j] = listaHSV_Cores_Canetas[min_dist_index][2]
        print(i,j)

hsv_img_out = cv2.merge((H_out,S_out,V_out))

img_out = cv2.cvtColor(hsv_img_out, cv2.COLOR_HSV2BGR)

# Display the image with contours
cv2.imshow('cores_finais', img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()

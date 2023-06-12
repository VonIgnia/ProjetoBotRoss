import cv2
import matplotlib.pyplot as plt

import numpy as np
from math import *
import Functions


img_in = cv2.imread("imgs_avancadas/birb.jpeg", cv2.IMREAD_COLOR)

if img_in is None:
    print("File not found. Bye!")
    exit(0)

gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
returns, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

cv2.imshow('original', img_in)
cv2.waitKey(0)
cv2.destroyAllWindows()


A4_retrato = (297,210) #dimensões em mm (height, width)
A4_paisagem = (210,297) #dimensões em mm (height, width)

resized_image = Functions.resize_keeping_aspect_ratio(img_in,A4_retrato)
cv2.imshow('Resized Image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#For HSV, hue range is [0,179], saturation range is [0,255], and value range is [0,255]
hsv_resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

[H,S,V] = cv2.split(hsv_resized_image)
(height,width) = H.shape

#fornecer cores de canetas no formato (H[0-360], S([0-100], V[0-100])
Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25]]

hsv_img_out = Functions.Simplifica_cores(img_in,Cores_Canetas)

simplified_colors = cv2.cvtColor(hsv_img_out, cv2.COLOR_HSV2BGR)

# Display the image with contours
cv2.imshow('cores_finais', simplified_colors)
cv2.waitKey(0)

img_out = cv2.cvtColor(hsv_img_out, cv2.COLOR_HSV2BGR)
for color in Cores_Canetas:
    print(color)
    for i in range(height-1):
        for j in range(width-1):

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


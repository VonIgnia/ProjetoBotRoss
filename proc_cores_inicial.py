import cv2
import matplotlib.pyplot as plt

import numpy as np
img_in = cv2.imread("imgs_avancadas\Lenna.png", cv2.IMREAD_COLOR)
if img_in is None:
    print("File not found. Bye!")
    exit(0)

[B,G,R] = cv2.split(img_in)
(height,width) = B.shape 

R_out = np.zeros((height,width), dtype = "uint8")
G_out = np.zeros((height,width), dtype = "uint8")
B_out = np.zeros((height,width), dtype = "uint8")

for i in range(height-1):
    for j in range(width-1):
        if R[i,j] > G[i,j] and R[i,j] > B[i,j]:
            R_out[i,j] = 255
        if G[i,j] > B[i,j]:
            G_out[i,j] = 255
        else:
            B_out[i,j]= 255

plt.imshow(R_out, cmap='gray')
plt.show()

plt.imshow(G_out, cmap='gray')
plt.show()

plt.imshow(B_out, cmap='gray')
plt.show()

img_out = cv2.merge((B_out,G_out,R_out))
plt.imshow(img_out, cmap='gray')
plt.show()
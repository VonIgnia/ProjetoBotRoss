import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import *

img_in = cv2.imread("imgs_iniciais\Cute-Cartoon-Panda.jpg", cv2.IMREAD_COLOR)
cv2.imshow('inicial', img_in)

inverted_image = cv2.bitwise_not(img_in)
cv2.imshow('imagem invertida', inverted_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

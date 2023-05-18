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

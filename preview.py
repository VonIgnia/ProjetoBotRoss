import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import *


#imagem do preview
image = np.zeros((500, 700), dtype=np.uint8)
#imagem que vai para o robo processar
real_image = np.zeros((500, 700, 3), dtype=np.uint8)

# desenhe o tamnaho das folhas na imagem
color = (100, 100, 100)  # White color (BGR format)
thickness = 1  # Thickness of the rectangle border
start_point = (0, 0)  # Top-left corner of the rectangle

end_point_a4 = (297 , 210)
end_point_a3 = (420 , 297)
end_point_a2 = (594 , 420)

cv2.rectangle(image, start_point, end_point_a4, color, thickness)
cv2.rectangle(image, start_point, end_point_a3, color, thickness)
cv2.rectangle(image, start_point, end_point_a2, color, thickness)


###############################################################################
#                       Gerar imagem
###############################################################################

img_in = cv2.imread("imgs_iniciais\Cute-Cartoon-Panda.jpg", cv2.IMREAD_GRAYSCALE)
papel = end_point_a4
margem = 0.1 # minima em % do papel
papel_escolhido = (papel[0]*(1-margem),papel[1]*(1-margem))

#descobrir qual a oritenação da imagem
height, width = img_in.shape
#gira para encaixar melhor, se necessario
if  height >= width:
    img_in = cv2.rotate(img_in, cv2.ROTATE_90_CLOCKWISE)
    height, width = img_in.shape

#faz as razoes de proporção por altura e largura
Razao_altura = papel_escolhido[1]/height
Razao_largura = papel_escolhido[0]/width
#escolhe a razão menor
if Razao_altura < Razao_largura:
    Ratio = Razao_altura
else: 
    Ratio = Razao_largura
#cria as novas dimensões da imagem e redimensiona
nova_altura = int(height*Ratio)
nova_largura = int(width*Ratio)
novo_tamanho_imagem = (nova_largura, nova_altura)
img_in = cv2.resize(img_in, novo_tamanho_imagem)


#centraliza a imagem e coloca no preview
margem_x = int((papel[0]-papel_escolhido[0])/2)
margem_y = int((papel[1]-papel_escolhido[1])/2)

image[margem_y:nova_altura+margem_y,margem_x:nova_largura+margem_x] = img_in

img_in = cv2.cvtColor(img_in, cv2.COLOR_GRAY2BGR)
real_image[margem_y:nova_altura+margem_y,margem_x:nova_largura+margem_x] = img_in

# Display the black image
cv2.imshow('Black Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
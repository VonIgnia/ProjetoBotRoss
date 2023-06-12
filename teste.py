import cv2
import numpy as np

def Gera_preenchimento_Vf(img_in):
    _, imagem_binarizada = cv2.threshold(img_in, 127, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(imagem_binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    Prototipo_lista_preenchimentos = []
    
    for contour in contours:
        filling_points = contour.squeeze().tolist()
        Prototipo_lista_preenchimentos.extend(filling_points)
        Prototipo_lista_preenchimentos.append([0, 0, 60])

    return imagem_binarizada, Prototipo_lista_preenchimentos

img_in = cv2.imread("imgs_iniciais\saopaulo.jpg", cv2.IMREAD_GRAYSCALE)
img_in = cv2.resize(img_in, (500,500))
img_preenchimento,lista_preenchimento = Gera_preenchimento_Vf(img_in)
cv2.imshow('Preview', img_preenchimento)
cv2.waitKey(0)
cv2.destroyAllWindows()
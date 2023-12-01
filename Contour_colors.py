#rodar com arquivo Contornos Done
import Functions
import cv2

listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25]]

img_in = cv2.imread("imgs_avancadas/birb.jpeg", cv2.IMREAD_COLOR)

contour_points = Functions.Gera_contornos_V3(img_in)

gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
_, imagem_binarizada = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
filling_points = Functions.Gera_preenchimento_V6(imagem_binarizada, listaHSV_Cores_Canetas)
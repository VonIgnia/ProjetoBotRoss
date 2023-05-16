import cv2

import numpy as np
import matplotlib.pyplot as plt

from math import *

f = plt.figure(figsize=(10,5))

img_in = cv2.imread("sonic_logo.jpg", cv2.IMREAD_COLOR)
if img_in is None:
    print("File not found. Bye!")
    exit(0)

Canny_edges = cv2.Canny(img_in, threshold1=100, threshold2=200, apertureSize=3)

#Separando os canais de cor da imagem original
[B,G,R] = cv2.split(img_in)
(height,width) = B.shape 
        
returns,thresh=cv2.threshold(Canny_edges,90,255,cv2.THRESH_BINARY_INV)
#returns,thresh=cv2.threshold(img_in,90,255,cv2.THRESH_BINARY)

#outra forma de detectar contornos (utiliza de 2 thresholds e aparentemente detecta tanto bordas de subida quanto bordas de descida)

contours,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
img1_text = cv2.cvtColor(img_in,cv2.COLOR_BGR2RGB)

#Define initial contour
initial = 2
#Define minimum length
minimum_length = 25

# Draw interior contours in red
contour_number = 0
dict_contour_points = {}

for i in range(initial,len(contours)):

    if hierachy[0][i][3] != -1:
        perimeter = cv2.arcLength(contours[i],True)
        #Draw contours with at least the minimum length
        if perimeter >= minimum_length:
            
            #Draw contours starting at initial count
            if contour_number >= initial:
                cv2.drawContours(img_in, contours, i, (0, 0, 255), 2)
                contour_points = []
                # o loop "for" a seguir tem como objetivo salvar os pontos de cada contorno detectado, separadamente uns dos outros,
                #assim permitindo chamar os contornos separadamente
                for point in contours[i]:
                    #point[0].append(0) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z
                    contour_points.append(point[0])
                    #print ("ponto",point[0], "do contorno:",i)
                
                dict_contour_points["Contorno{}".format(i)] = contour_points
            contour_number += 1

#print (len(dict_contour_points))
#print (len(dict_contour_points["Contorno3"]))

#número de contornos detectados
#print (len(dict_contour_points))

#print (dict_contour_points["Contorno1"])

#print(Canny_edges)

Prototipo_lista_contornos = []

#for i in dict_contour_points["Contorno1"]:
#    i = list(np.append(i,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z
#    Prototipo_lista_contornos.append(i)
#    print (i)

indice_interno = 0

i_atual=0
for i in dict_contour_points:
    for j in dict_contour_points[i]:
        
        j = list(np.append(j,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z
        #Prototipo_lista_contornos.append(j)

        if i != i_atual:
            Prototipo_lista_contornos.append(list(np.add(j,[0,0,60]))) #acrescenta movimento em Z no inicio do contorno para não rabiscar entre contornos
            print("Entrou")
            i_atual = i
        Prototipo_lista_contornos.append(j)

        print(j,i,indice_interno)
        indice_interno +=1

    #acrescenta movimento em Z no início do contorno para não rabiscar entre contornos
    Prototipo_lista_contornos.append(list(np.add(Prototipo_lista_contornos[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos
    #Prototipo_lista_contornos.insert(indice_interno, list(np.add(Prototipo_lista_contornos[0],[0,0,60])))
    
#print(Prototipo_lista_contornos)
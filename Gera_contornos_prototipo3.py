import cv2

import numpy as np
import matplotlib.pyplot as plt

from math import *

f = plt.figure(figsize=(10,5))

img_in = cv2.imread("imgs_iniciais/novapizza.webp", cv2.IMREAD_COLOR)
if img_in is None:
    print("File not found. Bye!")
    exit(0)

#Separando os canais de cor da imagem original
[B,G,R] = cv2.split(img_in)
(height,width) = B.shape 
        
#returns,thresh=cv2.threshold(img_in,90,255,cv2.THRESH_BINARY_INV)
returns,thresh=cv2.threshold(G,90,255,cv2.THRESH_BINARY)

#outra forma de detectar contornos (utiliza de 2 thresholds e aparentemente detecta tanto bordas de subida quanto bordas de descida)
Canny_edges = cv2.Canny(G,100,200)
contours,hierachy=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)


img1_text = cv2.cvtColor(img_in,cv2.COLOR_BGR2RGB)
#img1_text = cv2.cvtColor(B,cv2.COLOR_GRAY2RGB)

cv2.imshow('Image with Contours', thresh)


i=0
dict_contour_points = {}
for contour in contours:
    i+=1

    #numerar os contornos detectados
    M = cv2.moments(contour)         
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    
    cv2.drawContours(img1_text,contour,-1,(0,255,255),3)
    cv2.putText(img1_text, str(i), (cX,cY), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
    
    hull = cv2.convexHull(contour, returnPoints=True)
    #cv2.drawContours(img1_text,hull,-1,(0,255,0),5)
    
    #print ("Contorno", i, "Cx=", cX,"Cy=", cY)        
    contour_points = []
    
    # o loop "for" a seguir tem como objetivo salvar os pontos de cada contorno detectado, separadamente uns dos outros,
    #assim permitindo chamar os contornos separadamente
    for point in contour:
        #point[0].append(0) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z
        contour_points.append(point[0])
        #print ("ponto",point[0], "do contorno:",i)
    
    dict_contour_points["Contorno{}".format(i)] = contour_points

#print (len(dict_contour_points["Contorno1"]))
#print (len(dict_contour_points["Contorno3"]))

#número de contornos detectados
#print (len(dict_contour_points))

#print (dict_contour_points["Contorno1"])

plt.imshow(B, cmap='gray')
plt.show()          

plt.imshow(thresh, cmap='gray')
plt.show() 

#plt.imshow(Canny_edges, cmap='gray')
#plt.show() 

#plt.imshow(thresh, cmap='gray')
plt.imshow(img1_text, cmap='gray')
plt.show()          

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
    
print(Prototipo_lista_contornos)
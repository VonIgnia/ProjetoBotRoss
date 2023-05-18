#bibliotecas necesárias para o socket
import socket
import time

#bibliotecas necessárias para os contornos
import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import *

#As funções iniciais desse arquivo tiveram como base a Função Gera_Conornos_V3 do arquivo Functions

def Gera_Contornos(img_in):
    if img_in is None:
        print("File not found. Bye!")
        exit(0)

    #Separando os canais de cor da imagem original
    [B,G,R] = cv2.split(img_in)
    (height,width) = B.shape 
            
    #returns,thresh=cv2.threshold(img_in,90,255,cv2.THRESH_BINARY_INV)
    returns,thresh=cv2.threshold(B,90,255,cv2.THRESH_BINARY)

    #outra forma de detectar contornos (utiliza de 2 thresholds e aparentemente detecta tanto bordas de subida quanto bordas de descida)
    Canny_edges = cv2.Canny(B,100,200)
    contours,hierachy=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    return contours

#entre essas duas cabe um filtra contornos

def Gera_Lista_Pontos_Contorno(img_in, contours):
    img1_text = cv2.cvtColor(img_in,cv2.COLOR_BGR2RGB)
    
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
        
        #print ("Contorno", i, "Cx=", cX,"Cy=", cY)        
        contour_points = []
        
        # o loop "for" a seguir tem como objetivo salvar os pontos de cada contorno detectado, separadamente uns dos outros,
        #assim permitindo chamar os contornos separadamente
        for point in contour:
            #point[0].append(0) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z
            contour_points.append(point[0])

        #salva os pontos do contorno em um dicionário Contorno{numero do contorno}
        dict_contour_points["Contorno{}".format(i)] = contour_points

    Prototipo_lista_contornos = []

    i_atual = 0 #flag para checar se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
    
    for i in dict_contour_points: #para cada elemento(contorno(conjunto de pontos [x, y])) no dicionário
        for j in dict_contour_points[i]: #para cada ponto[x, y] no contorno:

            j = list(np.append(j,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z, esse valor sempre é 0
            if i != i_atual: #se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
                Prototipo_lista_contornos.append(list(np.add(j,[0,0,60]))) #acrescenta movimento em Z no inicio do contorno para não rabiscar entre contornos
                i_atual = i
            Prototipo_lista_contornos.append(j)


        Prototipo_lista_contornos.append(list(np.add(Prototipo_lista_contornos[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos
    return Prototipo_lista_contornos


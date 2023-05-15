#bibliotecas necesárias para o socket
import socket
import time

#bibliotecas necessárias para os contornos
import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import *


img_in = cv2.imread("shapes.jpg", cv2.IMREAD_COLOR)

def Gera_contornos_V1(img_in):
    if img_in is None:
        print("File not found. Bye!")
        exit(0)

    #Separando os canais de cor da imagem original
    [B,G,R] = cv2.split(img_in)

    #será usadou futuramente para calibrar o tamanho dos desenhos
    #(height,width) = B.shape 
            
    #returns,thresh=cv2.threshold(B,90,255,cv2.THRESH_BINARY_INV)
    returns,thresh=cv2.threshold(B,90,255,cv2.THRESH_BINARY)

    contours,hierachy=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

    #outra forma de detectar contornos (utiliza de 2 thresholds e aparentemente detecta tanto bordas de subida quanto bordas de descida)
    #Canny_edges = cv2.Canny(B,100,200)

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
        
        #print ("Contorno", i, "Cx=", cX,"Cy=", cY)        
        contour_points = []
        
        # o loop "for" a seguir tem como objetivo salvar os pontos de cada contorno detectado, 
        # separadamente uns dos outros, assim permitindo chamar os contornos separadamente.
        for point in contour:
            contour_points.append(point[0]) #acrescenta o Z á lista de pontos que antes continha apenas informações de X e de Y
            #print ("ponto",point[0], "do contorno:",i)
        
        dict_contour_points["Contorno{}".format(i)] = contour_points

    #número de contornos detectados
    #print (len(dict_contour_points))

    #print (dict_contour_points["Contorno1"])

    #plt.imshow(B, cmap='gray')
    #plt.show()          

    #plt.imshow(thresh, cmap='gray')
    #plt.show() 

    #plt.imshow(img1_text, cmap='gray')
    #plt.show()          

    Prototipo_lista_contornos = []

    for i in dict_contour_points["Contorno1"]:
        i = list(np.append(i,0))
        Prototipo_lista_contornos.append(i)
        #print (i)

    return Prototipo_lista_contornos

def Gera_contornos_V2(img_in):
    if img_in is None:
        print("File not found. Bye!")
        exit(0)

    #Separando os canais de cor da imagem original
    [B,G,R] = cv2.split(img_in)
    (height,width) = B.shape 
            
    #returns,thresh=cv2.threshold(B,90,255,cv2.THRESH_BINARY_INV)
    returns,thresh=cv2.threshold(B,90,255,cv2.THRESH_BINARY)

    contours,hierachy=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

    #outra forma de detectar contornos (utiliza de 2 thresholds e aparentemente detecta tanto bordas de subida quanto bordas de descida)
    Canny_edges = cv2.Canny(B,100,200)

    img1_text = cv2.cvtColor(img_in,cv2.COLOR_BGR2RGB)
    #img1_text = cv2.cvtColor(B,cv2.COLOR_GRAY2RGB)


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
        
        #hull = cv2.convexHull(contour, returnPoints=True)

        contour_points = []
        
        # o loop "for" a seguir tem como objetivo salvar os pontos de cada contorno detectado, separadamente uns dos outros, assim permitindo chamar os contornos separadamente
        for point in contour:
            contour_points.append(point[0])
            
        
        dict_contour_points["Contorno{}".format(i)] = contour_points

    Prototipo_lista_contornos = []

    indice_interno = 0

    i_atual=0
    for i in dict_contour_points:
        
        for j in dict_contour_points[i]:
            j = list(np.append(j,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z

            if i != i_atual:
                Prototipo_lista_contornos.append(list(np.add(j,[0,0,60]))) #acrescenta movimento em Z no inicio do contorno para não rabiscar entre contornos
                print("Entrou")
                i_atual = i
            
            Prototipo_lista_contornos.append(j)
            print(j,i,indice_interno)
            indice_interno +=1

        Prototipo_lista_contornos.append(list(np.add(Prototipo_lista_contornos[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos
   
    print(Prototipo_lista_contornos)
    return Prototipo_lista_contornos
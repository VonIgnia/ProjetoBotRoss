import cv2
import matplotlib.pyplot as plt

import numpy as np
from math import *
import FunctionsV2

import socket
import time
import threading


img_in = cv2.imread(FunctionsV2.select_image(), cv2.IMREAD_COLOR)
if img_in is None:
    print("File not found. Bye!")
    exit(0)

# Display the image as is imported
cv2.imshow('hsv', img_in)
cv2.waitKey(0)
cv2.destroyAllWindows()

A4_retrato = (297,210) #dimensões em mm (height, width)
A4_paisagem = (210,297) #dimensões em mm (height, width)

resized_image = FunctionsV2.resize_keeping_aspect_ratio(img_in,A4_retrato)
cv2.imshow('Resized Image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#imagem que o robô irá desenhar:
#img_v = cv2.flip(hsv_img_in_norm, 0) # flip the image by vertically
#img_h = cv2.flip(hsv_img_in_norm, 1) # flip the image by horizontally
#img_in_norm_vh = cv2.flip(hsv_resized_image,-1) # flip the image in both axis


#fornecer cores de canetas no formato (H[0-360], S([0-100], V[0-100])
#sem preto, nem branco
#listaHSV_Cores_Canetas =  [[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 48.2],[326, 71.9, 57.3],[0,0,0]]
#cores + preto e branco
listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25],[0,0,0]]

#lista reduzida para testes
#listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100]]

hsv_img_out = FunctionsV2.Simplify_Image_Colors(resized_image,listaHSV_Cores_Canetas)
simplified_colors = cv2.cvtColor(hsv_img_out, cv2.COLOR_HSV2BGR)

# Display the image with simplified colours
cv2.imshow('cores_finais', simplified_colors)
cv2.waitKey(0)

#print((img_out[0,0]))
(height,width) = (simplified_colors.shape[0], simplified_colors.shape[1])
img_out = simplified_colors
for color in listaHSV_Cores_Canetas:
    for i in range(height-1):
        for j in range(width-1):
            #print(hsv_img_out[i,j], "o", color)
            if np.all(hsv_img_out[i,j] == color):
                img_out[i,j] =  color
            else:
                img_out[i,j] = [0,0,0]

    img_out = cv2.cvtColor(img_out, cv2.COLOR_HSV2BGR)
    grayscale_colors =  cv2.cvtColor(img_out, cv2.COLOR_BGR2GRAY)
    returns, thresh = cv2.threshold(grayscale_colors, 1, 255, cv2.THRESH_BINARY)

    cv2.imshow(str(color), img_out)
    cv2.waitKey(0)

    point_positions = FunctionsV2.Generate_fillings(thresh)
    #cv2.imshow(str(color), thresh)
    #cv2.waitKey(0)
    
    print ('UR5 Communication')

    #HOST = '10.103.16.140'
    HOST = '10.103.16.11'
    PORT = 20000

    print('Trying Connection')
    count = 0

    connected = False
    while (connected == False):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        c, addr = s.accept()
        if (addr[0] != ''):
            connected = True
            print("Connected")
            
    lista=point_positions 
    lista.insert(0, list(np.add(lista[0],[0,0,60]))) #acrescenta movimento em Z no início do contorno para não rabiscar entre contornos
    lista.append(list(np.add(lista[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos

    T = len(lista)

    tam_max_comm = 10 #numero de pontos que serão passados a cada vez para o robo

    n_appends = tam_max_comm - ( T% tam_max_comm)
    print (n_appends)
    while n_appends != 0:
        lista.append([0,0,0])
        n_appends = n_appends-1

    T = len(lista)

    cpi = 0 #indica o indice do ponto atual na lista T(current point index)

    #enquanto o tamanho da lista que vai ser comunicada for menor do que o tamanho comunicável
    #percorrer cada elemento da lista e adicionar às listas que serão comunicadas
    pontos_enviados = 0

    print(lista)

    while pontos_enviados < T: #enquanto o indice do ponto atual for mentor que o compriomento total da lista de pontos
        if T - cpi < tam_max_comm: #se o numero de pontos da lista que faltam ser comunicados forem menores do que o valor de pontos que serão comunicados
            tam_max_comm = T-cpi   #numero de pontos que serão passados a cada vez para o robo

        X = [] #X ,Y e Z irão conter t_max_comm coordenadas
        Y = []
        Z = []
        while len(Z) < tam_max_comm:
            X.append(lista[cpi][0])
            Y.append(lista[cpi][1])
            Z.append(lista[cpi][2])
            cpi+=1

        try:
            c.send(str([tam_max_comm]).encode('ascii')) #tamanho das listas X, Y e Z
            print ("num_pontos", [tam_max_comm])
            time.sleep(0)
            c.send(str(X).encode('ascii')) #codifica (x,y,z,Rx,Ry,Rz) para um formato compreendido pelo robô
            print ("X", X)
            time.sleep(0)
            c.send(str(Y).encode('ascii')) #codifica (x,y,z,Rx,Ry,Rz) para um formato compreendido pelo robô
            print ("Y", Y)
            time.sleep(0)
            c.send(str(Z).encode('ascii')) #codifica (x,y,z,Rx,Ry,Rz) para um formato compreendido pelo robô
            print ("Z", Z)
            time.sleep(0)
        
        except socket.error as socketerror:
            print (count)

        pontos_enviados+=tam_max_comm
        count += 1


    c.close()
    s.close()
    print('Disconnected')
    print('Finished Colour')

#dictionary contining one binary image for each available color
#impossible to store image on dict (unhashable type: "list")
#dict_splited_colors = FunctionsV2.Split_Colors(simplified_colors,listaHSV_Cores_Canetas) 

cv2.destroyAllWindows()
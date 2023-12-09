#PT_BR bibliotecas para processamento de imagem
#US_EN libraries for image processing

import cv2
import matplotlib.pyplot as plt
import numpy as np
from pykuwahara import kuwahara
from math import *

#PT_BR arquivo criado pelos desenvolvedores para armazenar as funções e deixar o código mais limpo
#US_EN developer created file in order to store the functions and make a cleaner code here
import FunctionsV2

#PT_BR bibliotecas para comunicação com o UR5
#US_EN libraries for UR5 communication
import socket
import time
import logging
import threading

# Constants
HOST = '10.103.16.232'  # Replace with the actual IP address of your UR5 robot
PORT_COLOR = 30001
PORT_COORDINATES = 30002    # Replace with the desired port for sending data to the robot

#PORT_RECEIVE = 12346 # Replace with the desired port for receiving data from the robot

### Code

img_in = cv2.imread(FunctionsV2.select_image(), cv2.IMREAD_COLOR)
#img_in = cv2.imread("imgs_avancadas\Imagem1.png", cv2.IMREAD_COLOR)

if img_in is None:
    print("File not found. Bye!")
    exit(0)
height, width = img_in.shape[:2]
print("height: {}; width: {}".format(height, width))

A4_retrato = (297,210) #dimensões em mm (height, width)
A4_paisagem = (210,297) #dimensões em mm (height, width)

resized_image = FunctionsV2.resize_keeping_aspect_ratio(img_in,A4_paisagem)

resized_height, resized_width = resized_image.shape[:2]
print ("res height: {}; res width: {}".format(resized_height, resized_width))
cv2.imshow('resized_image',  resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#imagem que o robô irá desenhar:
#img_v = cv2.flip(hsv_img_in_norm, 0) # flip the image by vertically
#img_h = cv2.flip(hsv_img_in_norm, 1) # flip the image by horizontally
#img_in_norm_vh = cv2.flip(hsv_resized_image,-1) # flip the image in both axis

#cores + preto e branco
Rainbow_Pallete =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],
                           [214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25],[0,0,10]]

SkinTones_Pallete = [[0,0,100],[0,100,80],[24,100,100],[60,100,100],[34,53,88],[34,68,77],[34,49,99],[137,85.5,43.1],[0,0,10]]

RedGrenBluYe = [[0,0,100],[0,100,80],[60,100,100],[137,85.5,43.1],[197,70,83.5],[0,0,10]]

listaHSV_Cores_Canetas = RedGrenBluYe
#listaHSV_Cores_Canetas = SkinTones_Pallete

#lista reduzida para testes (cores quentes)
#listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100]]

#lista reduzida para testes (cores frias)
#listaHSV_Cores_Canetas =  [[0,0,100],[197,70,83.5],[214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25]]

simplified_colors = FunctionsV2.Simplify_Image_Colors(resized_image,listaHSV_Cores_Canetas)
simplified_colors_RGB = cv2.cvtColor(simplified_colors, cv2.COLOR_HSV2BGR)

# Display the image with simplified colours
cv2.imshow('cores_finais', simplified_colors_RGB)
cv2.waitKey(0)
cv2.destroyAllWindows()

dict_filings_by_color = FunctionsV2.Split_Colors(simplified_colors, listaHSV_Cores_Canetas)
dict_point_positions_by_color = {}


"########################################### SOCKET COLOR START #################################################"

print('Trying Color Socket Connection')
count = 0

Color_socket_connected = False
while (Color_socket_connected == False):
    Color_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Color_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Color_socket.bind((HOST, PORT_COLOR))
    Color_socket.listen(5)
    Color_socket_c, Color_socket_addr = Color_socket.accept()
    if (Color_socket_addr[0] != ''):
        Color_socket_connected = True
        print("Color_socket_connected")

for color in dict_filings_by_color.keys():
    "############################################ socket coordinates start #############################################################################################"

    #Checking if UR is ready to recieve color: color must be done by the start
    ready_to_recieve_color = Color_socket_c.recv(1024)
    #while UR is not ready to recieve color info wait until UR is ready
    while ready_to_recieve_color != b"ready":
        print (ready_to_recieve_color)
        time.sleep(0.5)

    #when color is done create a new Coordinates_Socket
    print('Trying Coordinate Socket Connection')
    Coord_socket_connected = False
    while (Coord_socket_connected == False):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT_COORDINATES))
        s.listen(5)
        c, addr = s.accept()
        if (addr[0] != ''):
            Coord_socket_connected = True
            print("Coordinate socket {} connected".format(color))

    RGB_split_preview = cv2.cvtColor(dict_filings_by_color[color], cv2.COLOR_HSV2BGR)
    #cv2.imshow(color, RGB_split_preview)
    #cv2.waitKey(0)
    
    binirized_color =  cv2.cvtColor(dict_filings_by_color[color], cv2.COLOR_BGR2GRAY)
    returns, thresh = cv2.threshold(binirized_color, 1, 255, cv2.THRESH_BINARY)
    point_positions = FunctionsV2.Generate_fillings(thresh, color)
        
    lista=point_positions 

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
            print ("num_pontos", tam_max_comm)
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

    Robot_operation = c.recv(1024)
    if Robot_operation == b"robot_operation_done":
        print("Robot Operation")
        Color = "Color is done"
        Color_socket_c.send(Color.encode('ascii'))
    print ("ColorisDone")

    c.close()
    s.close()
    print('Coordinate Socket Disconnected')
    print('Finished Color {}'.format(color))

    
"############################################ socket coordenadas end #############################################################################################"

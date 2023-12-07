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

point_positions = [[0,0,0]]
for i in range(1, 101):
    point_positions.append([0, i, 0])

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

#Checking if color Done: color must be done by the start
ready_to_recieve_color = Color_socket_c.recv(1024)
#print ("ouvindo {}".format(ready_to_recieve_color))

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
        print("Coordinate socket connected")

"############################################ socket coordinates start #############################################################################################"
 
lista=point_positions 
lista.insert(0, list(np.add(lista[0],[0,0,60]))) #acrescenta movimento em Z no início do contorno para não rabiscar entre contornos
lista.append(list(np.add(lista[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos

T = len(lista)

tam_max_comm = 10 #numero de pontos que serão passados a cada vez para o robo

n_appends = tam_max_comm - ( T% tam_max_comm)
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
    
#Color = "Color is done"
#Color_socket_c.send(Color.encode('ascii'))
#Robot_operation = "Robot finished color"
Robot_operation = c.recv(1024)
if Robot_operation == b"robot_operation_done":
    print("Robot Operation")
    Color = "Color is done"
    Color_socket_c.send(Color.encode('ascii'))
print ("ColorisDone")

c.close()
s.close()
print('Coordinate Socket Disconnected')
print('Finished Color')
 
"############################################ socket end #############################################################################################"

print ('Program Started')
print('Trying Connection')
count = 0
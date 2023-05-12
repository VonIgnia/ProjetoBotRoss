import socket
import time

import Functions
import numpy as np
import cv2

print ('Program Started')

HOST = '10.103.16.140'
PORT = 20000

print('Trying Connection')
count = 0

img_in = cv2.imread("shapes.jpg", cv2.IMREAD_COLOR)
point_positions = Functions.Gera_contornos_V1(img_in)

lista = point_positions
lista.insert(0, list(np.add(lista[0],[0,0,60]))) #acrescenta movimento em Z no contorno para não rabiscar entre contornos
lista.append(list(np.add(lista[-1],[0,0,60])))   #acrescenta movimento em Z no contorno para não rabiscar entre contornos

T = len(lista)

tam_max_comm = 20 #numero de pontos que serão passados a cada vez para o robo
cpi = 0 #indica o indice do ponto atual na lista T(current point index)

#enquanto o tamanho da lista que vai ser comunicada for menor do que o tamanho comunicável
#percorrer cada elemento da lista e adicionar às listas que serão comunicadas

while cpi < T:
    #se o numero de pontos da lista que faltam ser comunicados forem menores do que o valor de pontos que serão comunicados
    if T - cpi < tam_max_comm:
        tam_max_comm = T-cpi #numero de pontos que serão passados a cada vez para o robo
    X = []
    Y = []
    Z = []
    while len(Z) < tam_max_comm:
        X.append(lista[cpi][0])
        Y.append(lista[cpi][1])
        Z.append(lista[cpi][2])
        cpi+=1

    print ("num_pontos", tam_max_comm)
    print ("X", X)
    print ("Y", Y)
    print ("Z", Z)
    time.sleep(5)

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

print(addr)

c.send(str(tam_max_comm).encode('ascii'))
while (count < tam_max_comm):
    try:
        time.sleep(0.5)
        c.send(str(tuple(point_positions*count)).encode('ascii')) #codifica (x,y,z,Rx,Ry,Rz) para um formato compreendido pelo robô
        print(tuple(point_positions*count))
        
    except socket.error as socketerror:
        print (count)
    count += 1

c.close()
s.close()
print('Disconnected')
print('Program Finished')

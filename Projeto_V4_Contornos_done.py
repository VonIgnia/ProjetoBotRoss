#rodar com arquivo Contornos Done
import socket
import time

import Functions
import numpy as np
import cv2

print ('Program Started')

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

img_in = cv2.imread("imgs_iniciais/red.png", cv2.IMREAD_COLOR)

A4_paisagem = (297,210) #dimensões em mm (width, height)
resized = Functions.resize_keeping_aspect_ratio(img_in,A4_paisagem)

#point_positions = Functions.Gera_contornos_V3(resized)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
# Apply binary thresholding
_, imagem_binarizada = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
point_positions = Functions.Gera_preenchimento_Vf(imagem_binarizada)

lista = point_positions
lista.insert(0, list(np.add(lista[0],[0,0,60]))) #acrescenta movimento em Z no início do contorno para não rabiscar entre contornos
lista.append(list(np.add(lista[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos

T = len(lista)

tam_max_comm = 10 #numero de pontos que serão passados a cada vez para o robo

n_appends = tam_max_comm - (T % tam_max_comm)
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

    #time.sleep(2)


c.close()
s.close()
print('Disconnected')
print('Program Finished')

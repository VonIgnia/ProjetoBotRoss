
import socket
import time
import sys
import Functions
import numpy as np
import cv2

print ('Program Started')

img_in = cv2.imread("imgs_avancadas\cartoon-robot-coloring-page.png", cv2.IMREAD_GRAYSCALE)
point_positions = Functions.escala_imagem(img_in)

x = input('Deseja continuar? (rode o programa no UR antes) ')
if x == '':
    sys.exit()

HOST = '10.103.16.140'
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

#inverter as coordenadas de y para funcionar no plano botross
for pontos in point_positions:
    pontos[1] = 200-pontos[1]

lista = []
linha = 0
num_linhas = 10

lista = point_positions
lista.insert(0, list(np.add(lista[0],[0,0,60]))) #acrescenta movimento em Z no início do contorno para não rabiscar entre contornos
lista.append(list(np.add(lista[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos

T = len(lista)

tam_max_comm = 10 #numero de pontos que serão passados a cada vez para o robo

n_appends = tam_max_comm - (T % tam_max_comm)
#print (n_appends)
while n_appends != 0:
    lista.append([0,0,0])
    n_appends = n_appends-1

T = len(lista)

cpi = 0 #indica o indice do ponto atual na lista T(current point index)

#enquanto o tamanho da lista que vai ser comunicada for menor do que o tamanho comunicável
#percorrer cada elemento da lista e adicionar às listas que serão comunicadas
pontos_enviados = 0

#print(lista)

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
        #print ("num_pontos", [tam_max_comm])

        c.send(str(X).encode('ascii')) #codifica (x,y,z,Rx,Ry,Rz) para um formato compreendido pelo robô
        #print ("X", X)

        c.send(str(Y).encode('ascii')) #codifica (x,y,z,Rx,Ry,Rz) para um formato compreendido pelo robô
        #print ("Y", Y)

        c.send(str(Z).encode('ascii')) #codifica (x,y,z,Rx,Ry,Rz) para um formato compreendido pelo robô
        #print ("Z", Z)

        
    except socket.error as socketerror:
        print (count)

    pontos_enviados+=tam_max_comm
    count += 1

c.close()
s.close()
print('Disconnected')
print('Program Finished')

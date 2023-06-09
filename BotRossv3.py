import socket
import time

import Functions
import numpy as np
import cv2

print ('Program Started')

# Get the local host name
myHostName = socket.gethostname()
print("Name of the localhost is {}".format(myHostName))


# Get the IP address of the local host
myIP = socket.gethostbyname(myHostName)
print("IP address of the localhost is {}".format(myIP))

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

img_in = cv2.imread("imgs_iniciais\shapes.jpg", cv2.IMREAD_COLOR)
point_positions = Functions.Gera_contornos_V3(img_in)

#gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
# Apply binary thresholding
#_, imagem_binarizada = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
#point_positions = Functions.Gera_preenchimento_V3(imagem_binarizada)


lista = []
linha = 0
num_linhas = 10

#while linha<num_linhas:
#    lista.append([0,linha*5,0])
#    lista.append([180,linha*5,0])
#    lista.append([180,linha*5,60])
#    lista.append([0,linha*5,60])
#    linha+=1
#print (lista)

#lista = [[0,0,0],[180,0,0],[180,5,0],[0,5,0],[0,10,0],[180,10,0]]
lista = point_positions
#lista.insert(0, list(np.add(lista[0],[0,0,60]))) #acrescenta movimento em Z no início do contorno para não rabiscar entre contornos
#lista.append(list(np.add(lista[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos

T = len(lista)

tam_max_comm = 10 #numero de pontos que serão passados a cada vez para o robo
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

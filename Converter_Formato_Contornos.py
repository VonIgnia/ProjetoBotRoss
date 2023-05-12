import time
import numpy as np

lista = [[120,60,10],[60,120,0],[0,120,0],[0,0,0],[60,120,60]] #pontos em formato [[x1,y1,z1],[x2,y2,z2]...]

lista.insert(0, list(np.add(lista[0],[0,0,60]))) #acrescenta movimento em Z no contorno para não rabiscar entre contornos
lista.append(list(np.add(lista[-1],[0,0,60])))   #acrescenta movimento em Z no contorno para não rabiscar entre contornos

T = len(lista)

tam_max_comm = 2 #numero de pontos que serão passados a cada vez para o robo
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




lista = [[120,60,10],[60,120,0],[0,120,0],[0,0,0],[60,120,60]]

X = []
Y = []
Z = []

T = len(lista) #pontos em formato [[x1,y1,z1],[x2,y2,z2]...]
tam_max_comm = 2 #numero de pontos que serão passados simultaneamente para o robo

#enquanto o tamanho da lista que vai ser comunicada for menor do que o tamanho comunicável
    #percorrer cada elemento da lista e adicionar às listas que serão comunicadas
itens_enviados = 0
while itens_enviados <= T:
    for i in lista:
        X.append(i[0])
        Y.append(i[1])
        Z.append(i[2])
        if len(Z) == tam_max_comm:
            break
    print ("X", X)
    print ("Y", Y)
    print ("Z", Z)
    itens_enviados += 1 







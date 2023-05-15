
#teste_preenchimento1 linha a linha (estratégia zig de usinagem)
lista = []
linha = 0
num_linhas = 10

while linha<num_linhas:
    lista.append([0,linha*5,0])
    lista.append([180,linha*5,0])
    lista.append([180,linha*5,60])
    lista.append([0,linha*5,60])
    linha+=1

print (lista)
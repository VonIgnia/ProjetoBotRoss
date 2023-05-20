#bibliotecas necesárias para o socket
import socket
import time

#bibliotecas necessárias para os contornos
import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import *

def resize_keeping_aspect_ratio(img_in, tamanho_folha):
    current_height, current_width = img_in.shape[:2]
    width = tamanho_folha[0]
    height = tamanho_folha[1]

    if height>width:
        width = 0
    
    if width>height:
        height = 0

    if width == 0:
        # Calculate the ratio based on the desired height
        ratio = height / float(current_height)
        new_width = int(current_width * ratio)
        new_height = height
    else:
        # Calculate the ratio based on the desired width
        ratio = width / float(current_width)
        new_width = width
        new_height = int(current_height * ratio)
    
    resized_img_in = cv2.resize(img_in, (new_width, new_height))
    
    #imagem que o robô irá desenhar:
    #img_v = cv2.flip(hsv_img_in_norm, 0) # flip the image by vertically
    #img_h = cv2.flip(hsv_img_in_norm, 1) # flip the image by horizontally
    img_out = cv2.flip(resized_img_in,-1) # flip the image in both axis

    return img_out

def Gera_contornos_V3(img_in):
    if img_in is None:
        print("File not found. Bye!")
        exit(0)

    #Separando os canais de cor da imagem original
    [B,G,R] = cv2.split(img_in)
            
    #returns,thresh=cv2.threshold(img_in,90,255,cv2.THRESH_BINARY_INV)
    returns,thresh=cv2.threshold(B,90,255,cv2.THRESH_BINARY)

    #outra forma de detectar contornos (utiliza de 2 thresholds e aparentemente detecta tanto bordas de subida quanto bordas de descida)
    Canny_edges = cv2.Canny(B,100,200)
    contours,hierachy=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)


    img1_text = cv2.cvtColor(img_in,cv2.COLOR_BGR2RGB)
    #img1_text = cv2.cvtColor(B,cv2.COLOR_GRAY2RGB)

    cv2.imshow('Image with Contours', thresh)

    #para cada contorno na lista contornos: numera o contorno, salva os pontos do contorno em um dicionário contorno{numero do contorno}
    i=0
    dict_contour_points = {}
    for contour in contours:
        i+=1

        #numerar os contornos detectados
        M = cv2.moments(contour)         
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        
        cv2.drawContours(img1_text,contour,-1,(0,255,255),3)
        cv2.putText(img1_text, str(i), (cX,cY), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
        
        #print ("Contorno", i, "Cx=", cX,"Cy=", cY)        
        contour_points = []
        
        # o loop "for" a seguir tem como objetivo salvar os pontos de cada contorno detectado, separadamente uns dos outros,
        #assim permitindo chamar os contornos separadamente
        for point in contour:
            contour_points.append(point[0])

        #salva os pontos do contorno em um dicionário Contorno{numero do contorno}
        dict_contour_points["Contorno{}".format(i)] = contour_points

    Prototipo_lista_contornos = []

    i_atual = 0 #flag para checar se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
    
    for i in dict_contour_points: #para cada elemento(contorno(conjunto de pontos [x, y])) no dicionário
        for j in dict_contour_points[i]: #para cada ponto[x, y] no contorno:

            j = list(np.append(j,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z, esse valor sempre é 0
            if i != i_atual: #se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
                Prototipo_lista_contornos.append(list(np.add(j,[0,0,60]))) #acrescenta movimento em Z no inicio do contorno para não rabiscar entre contornos
                i_atual = i
            Prototipo_lista_contornos.append(j)

        Prototipo_lista_contornos.append(list(np.add(Prototipo_lista_contornos[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos
    return Prototipo_lista_contornos

def Gera_preenchimento_V1(imagem_binarizada,distancia_linha=10,grossura_linha=8):
    
    # Set the size and separation of the lines
    height, width = imagem_binarizada.shape[:2]
    line_spacing = distancia_linha
    line_thickness = grossura_linha

    # Draw horizontal lines on the binary image
    for y in range(0, height, line_spacing):
        cv2.line(imagem_binarizada, (0, y), (width, y), 0, line_thickness)

    # Find contours
    contours, hierarchy = cv2.findContours(imagem_binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    i=0
    dict_filling_points = {}
    for contour in contours:
        i+=1

        filling_points = []

        for point in contour:
            filling_points.append(point[0])

        dict_filling_points["Preenchimento{}".format(i)] = filling_points

        #for point in filling_points:
        #    print(point[0])
        #    dist_from_start = sqrt()

    Prototipo_lista_preenchimentos = []

    i_atual = 0 #flag para checar se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
    
    for i in dict_filling_points: #para cada elemento(contorno(conjunto de pontos [x, y])) no dicionário
        for j in dict_filling_points[i]: #para cada ponto[x, y] no contorno:

            j = list(np.append(j,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z, esse valor sempre é 0
            if i != i_atual: #se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
                Prototipo_lista_preenchimentos.append(list(np.add(j,[0,0,60]))) #acrescenta movimento em Z no inicio do contorno para não rabiscar entre contornos
                i_atual = i
            Prototipo_lista_preenchimentos.append(j)


        Prototipo_lista_preenchimentos.append(list(np.add(Prototipo_lista_preenchimentos[-1],[0,0,60]))) #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos

    return Prototipo_lista_preenchimentos

def Gera_preenchimento_V2(imagem_binarizada,distancia_linha=10,grossura_linha=8):
    
    # Set the size and separation of the lines
    height, width = imagem_binarizada.shape[:2]
    line_spacing = distancia_linha
    line_thickness = grossura_linha

    # Draw horizontal lines on the binary image
    for y in range(0, height, line_spacing):
        cv2.line(imagem_binarizada, (0, y), (width, y), 0, line_thickness)

    # Find contours
    contours, hierarchy = cv2.findContours(imagem_binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    i=0
    dict_filling_points = {}
    for contour in contours:
        i+=1

        filling_points = []

        for point in contour:
            filling_points.append(point[0])

        fill_line = []
        dist=[]
        for element in filling_points:
            x_start = (point[0][0])
            #y_start = (point[0][1])

            x_end = (element[0])
            #y_end = (element[1])
            dist_from_start = sqrt((x_start - x_end)**2)
            dist.append(dist_from_start)
            
        max_dist = np.argmax(dist)
        #print(dist)
        #print(max_dist)
        
        fill_line.append(filling_points[0])
        fill_line.append(filling_points[max_dist])
        
        #print(fill_line)

        dict_filling_points["Preenchimento{}".format(i)] = fill_line 

    Prototipo_lista_preenchimentos = []

    i_atual = 0 #flag para checar se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
    
    for i in dict_filling_points: #para cada elemento(contorno(conjunto de pontos [x, y])) no dicionário
        for j in dict_filling_points[i]: #para cada ponto[x, y] no contorno:

            j = list(np.append(j,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z, esse valor sempre é 0
            if i != i_atual: #se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
                Prototipo_lista_preenchimentos.append(list(np.add(j,[0,0,60]))) #acrescenta movimento em Z no inicio do contorno para não rabiscar entre contornos
                i_atual = i
            Prototipo_lista_preenchimentos.append(j)

        Prototipo_lista_preenchimentos.append(list(np.add(Prototipo_lista_preenchimentos[-1],[0,0,60]))) #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos
        print (Prototipo_lista_preenchimentos)
    return Prototipo_lista_preenchimentos

def Simplifica_cores(img_in, listaHSV_Cores_disponiveis, kH = 1, kS = 1 , kV = 1):
    
    hsv_resized_image = cv2.cvtColor(img_in, cv2.COLOR_BGR2HSV)
    [H,S,V] = cv2.split(hsv_resized_image)
    (height,width) = H.shape

    listaHSV_Cores_Canetas =  [[0,0,100],[0,100,80],[24,100,100],[60,100,100],[137,85.5,43.1],[197,70,83.5],[214, 94.3, 64.7],[326, 71.9, 57.3],[240,80,25]]
    for cor in listaHSV_Cores_Canetas:
        cor[0] = int(np.clip((cor[0])/2,0,255))
        cor[1] = int(np.clip((cor[1]*255)/100,0,255))
        cor[2] = int(np.clip((cor[2]*255)/100,0,255))
    #print (listaHSV_Cores_Canetas)

    H_out = np.zeros((height,width), dtype = "uint8")
    S_out = np.zeros((height,width), dtype = "uint8")
    V_out = np.zeros((height,width), dtype = "uint8")

    for i in range(height-1):
        for j in range(width-1):
            vci = [H[i,j],S[i,j],V[i,j]] #vetor cor imagem
            lista_dist_eclidiana = []
            for vcc in listaHSV_Cores_Canetas: #vcc = vetor cor canetas

                dist_euclidiana = sqrt(((vcc[0]-vci[0])**2)*kH + ((vcc[1]-vci[1])**2)*kS + ((vcc[2]-vci[2])**2)*kV)
                lista_dist_eclidiana.append(dist_euclidiana)

            min_dist_index = np.argmin(lista_dist_eclidiana)
            H_out[i,j] = listaHSV_Cores_Canetas[min_dist_index][0]
            S_out[i,j] = listaHSV_Cores_Canetas[min_dist_index][1]
            V_out[i,j] = listaHSV_Cores_Canetas[min_dist_index][2]
            #print(i,j)

    hsv_img_out = cv2.merge((H_out,S_out,V_out))

    return 0

def Split_cores(img_in, lista_cores_disponiveis):
    (height,width) = (img_in.shape[0], img_in.shape[1])
    for color in lista_cores_disponiveis:

        for i in range(height-1):
            for j in range(width-1):
                #print(hsv_img_out[i,j], "o", color)
                if np.all(img_in[i,j] == color):
                    img_out[i,j] =  color
                else:
                    img_out[i,j] = [0,0,0]
        img_out = cv2.cvtColor(img_out, cv2.COLOR_HSV2BGR)
        cv2.imshow(str(color), img_out)
        cv2.waitKey(0)
        return (img_out)

    
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
        
    else:
        # Calculate the ratio based on the desired width
        ratio = width / float(current_width)

    new_width = int(current_width * ratio)
    new_height = int(current_height * ratio)
    resized_img_in = cv2.resize(img_in, (new_width, new_height))
    
    #imagem que o robô irá desenhar:
    #img_v = cv2.flip(hsv_img_in_norm, 0) # flip the image by vertically
    #img_h = cv2.flip(hsv_img_in_norm, 1) # flip the image by horizontally
    #img_vh = cv2.flip(resized_img_in,-1) # flip the image in both axis
    
    img_out = cv2.flip(resized_img_in, 1)
    img_out = cv2.flip(img_out,-1)

    return img_out

def Gera_contornos_Vf(img_in):
    _, thresh = cv2.threshold(img_in, 90, 255, cv2.THRESH_BINARY)

    
    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    
    # Draw the contours on a black image
    height, width = img_in.shape
    image = np.zeros((height, width), dtype=np.uint8)
    cv2.drawContours(image, contours, -1, (255, 255, 255), 2)

    # Initialize the list of contour points with added z-coordinate
    prototipo_lista_contornos = []

    for contour in contours:
        # Add the starting z-coordinate for each contour
        prototipo_lista_contornos.append([contour[0][0][0], contour[0][0][1], 20])

        for point in contour:
            # Add the x, y, and z coordinates to the list
            prototipo_lista_contornos.append([point[0][0], point[0][1], 0])

        # Add the ending z-coordinate for each contour
        prototipo_lista_contornos.append([contour[-1][0][0], contour[-1][0][1], 20])

    return image,prototipo_lista_contornos

def Gera_preenchimento_Vf(img_in,distancia_linha=10,grossura_linha=8):

    _, imagem_binarizada = cv2.threshold(img_in, 127, 255, cv2.THRESH_BINARY_INV)
    
    height, width = imagem_binarizada.shape[:2]
    line_spacing = distancia_linha
    line_thickness = grossura_linha

    # Draw horizontal lines on the binary image
    for y in range(0, height, line_spacing):
        cv2.line(imagem_binarizada, (0, y), (width, y), 0, line_thickness)

    # Display the binary image
    #cv2.imshow('Masked Image', imagem_binarizada)
    #cv2.waitKey(0)

    # Find contours
    contours, hierarchy = cv2.findContours(imagem_binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    i=0
    dict_filling_points = {}
    for contour in contours:
        i+=1
        filling_points = []
        
        x,y,w,h = cv2.boundingRect(contour)
        filling_points.append([x,y])
        filling_points.append([x+w,y])
        
        cv2.rectangle(imagem_binarizada,(x,y),(x+w,y+h),(255,255,255),1)
        
        #print (filling_points)
        

        #for point in contour:
        #    filling_points.append(point[0])

        dict_filling_points["Preenchimento{}".format(i)] = filling_points

    Prototipo_lista_preenchimentos = []

    i_atual = 0 #flag para checar se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
    
    for i in dict_filling_points: #para cada elemento(contorno(conjunto de pontos [x, y])) no dicionário
        for j in dict_filling_points[i]: #para cada ponto[x, y] no contorno:

            j = list(np.append(j,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z, esse valor sempre é 0
            if i != i_atual: #se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
                Prototipo_lista_preenchimentos.append(list(np.add(j,[0,0,60]))) #acrescenta movimento em Z no inicio do contorno para não rabiscar entre contornos
                i_atual = i
            Prototipo_lista_preenchimentos.append(j) #acrescenta o ponto [x,y,z] na lista
        Prototipo_lista_preenchimentos.append(list(np.add(Prototipo_lista_preenchimentos[-1],[0,0,60]))) #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos
    
    return imagem_binarizada,Prototipo_lista_preenchimentos

def Gera_preenchimento_V5(imagem_binarizada):
    # Display the binary image
    #cv2.imshow('Binary Image', imagem_binarizada)

    height, width = imagem_binarizada.shape[:2]
    line_coordinates = []

    for y in range(0, height, 15):
        line_start = None  # Start coordinate of the current line
        line_end = None  # End coordinate of the current line
        for x in range(width):
            if imagem_binarizada[y, x] == 255:
                if line_start is None:
                    line_start = (x, y)
                line_end = (x, y)
            elif line_start is not None:
                # Store the start and end coordinates of the line segment in line_coordinates
                line_coordinates.append((line_start, line_end))
                line_start = None
                line_end = None
        # Check if the line segment extends till the end of the row
        if line_start is not None and line_end is not None:
            line_coordinates.append((line_start, line_end))


    # Create a new blank black image to visualize the lines
    output_image = np.zeros((height, width), dtype=np.uint8)

    # Draw lines on the output image using the line coordinates
    for start, end in line_coordinates:
        cv2.line(output_image, start, end, 255, 1)


    # Create a new list to store the line coordinates with z-coordinate
    line_coordinates_3d = []

    # Define the z-coordinate values
    z_values = [20, 0, 0, 20]

    # Iterate through the line_coordinates list and apply the steps to add z-coordinate
    for i in range(len(line_coordinates)):
        x_start, y_start = line_coordinates[i][0]
        x_end, y_end = line_coordinates[i][1]
        
        # Step 1: Add the first coordinate with z = 20
        line_coordinates_3d.append([x_start, y_start, z_values[0]])
        
        # Step 2: Repeat the same element with z = 0
        line_coordinates_3d.append([x_start, y_start, z_values[1]])
        
        # Step 3: Add the next coordinate with z = 0
        line_coordinates_3d.append([x_end, y_end, z_values[1]])
        
        # Step 4: Repeat the same element with z = 20
        line_coordinates_3d.append([x_end, y_end, z_values[0]])


    print(line_coordinates_3d)

    #cv2.imshow('Output Image', output_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return line_coordinates_3d

def Simplifica_cores(img_in, listaHSV_Cores_Canetas, kH = 1, kS = 1 , kV = 1):
    
    hsv_resized_image = cv2.cvtColor(img_in, cv2.COLOR_BGR2HSV)
    [H,S,V] = cv2.split(hsv_resized_image)
    (height,width) = H.shape

    for cor in listaHSV_Cores_Canetas:
        cor[0] = int(np.clip((cor[0])/2,0,255))
        cor[1] = int(np.clip((cor[1]*255)/100,0,255))
        cor[2] = int(np.clip((cor[2]*255)/100,0,255))

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

    hsv_img_out = cv2.merge((H_out,S_out,V_out))

    return hsv_img_out

def Split_cores(img_in, lista_cores_disponiveis):
    (height,width) = (img_in.shape[0], img_in.shape[1])
    
    for color in lista_cores_disponiveis:
        img_out = img_in
        for i in range(height-1):
            for j in range(width-1):
                #print(hsv_img_out[i,j], "o", color)
                if np.all(img_in[i,j] == color):
                    img_out[i,j] = color
                else:
                    img_out[i,j] = [0,0,0]
        img_out = cv2.cvtColor(img_out, cv2.COLOR_HSV2BGR)
        cv2.imshow(str(color), img_out)
        cv2.waitKey(0)
        return img_out

def Gera_preenchimento_V6(img_in,lista_cores, line_spacing=10,line_thickness=8): #prevê as trocas de ferramentas
    height, width = imagem_binarizada.shape[:2]

    # Draw horizontal lines on the binary image
    for y in range(0, height, line_spacing):
        cv2.line(imagem_binarizada, (0, y), (width, y), 0, line_thickness)

    # Find contours
    contours, hierarchy = cv2.findContours(imagem_binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    filling_color_index = 0
    dict_filling_colors = {}
    for color in lista_cores:
        filling_color_index+=1
        
        filling_index = 0
        dict_filling_points = {}
        for contour in contours:
            filling_index+=1
            
            filling_points = []
            #finding contour bonding box in order to define its extension
            x,y,w,h = cv2.boundingRect(contour)
            filling_points.append([x,y])
            filling_points.append([x+w,y])
            
            cv2.rectangle(imagem_binarizada,(x,y),(x+w,y+h),(255,255,255),5)
            #appending trajectory points to a dictionary in order to split up different countour/ fillings
            dict_filling_points["Preenchimento{}".format(filling_index)] = filling_points
        dict_filling_colors["Preenchimento cor {}".format(filling_color_index)] = dict_filling_points
    print (dict_filling_colors)

    Prototipo_lista_preenchimentos = []

    i_atual = 0 #flag para checar se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
    
    for i in dict_filling_points: #para cada elemento(contorno(conjunto de pontos [x, y])) no dicionário
        for j in dict_filling_points[i]: #para cada ponto[x, y] no contorno:

            j = list(np.append(j,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z, esse valor sempre é 0
            if i != i_atual: #se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
                Prototipo_lista_preenchimentos.append(list(np.add(j,[0,0,60]))) #acrescenta movimento em Z no inicio do contorno para não rabiscar entre contornos
                i_atual = i
            Prototipo_lista_preenchimentos.append(j) #acrescenta o ponto [x,y,z] na lista
        Prototipo_lista_preenchimentos.append(list(np.add(Prototipo_lista_preenchimentos[-1],[0,0,60]))) #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos
    
    #cv2.imshow('Masked Image', imagem_binarizada)
    #cv2.waitKey(0)
    print (Prototipo_lista_preenchimentos)

    return Prototipo_lista_preenchimentos

    return 0    

def escala_imagem(img_in,papel=(297 , 210),margem=0.1):
    #imagem do preview
    image = np.zeros((500, 700), dtype=np.uint8)

    # desenhe o tamnaho das folhas na imagem
    color = (100, 100, 100)  # White color (BGR format)
    thickness = 1  # Thickness of the rectangle border
    start_point = (0, 0)  # Top-left corner of the rectangle

    end_point_a4 = (297 , 210)
    end_point_a3 = (420 , 297)
    end_point_a2 = (594 , 420)

    cv2.rectangle(image, start_point, end_point_a4, color, thickness)
    cv2.rectangle(image, start_point, end_point_a3, color, thickness)
    cv2.rectangle(image, start_point, end_point_a2, color, thickness)

    ###############################################################################
    #                       Gerar imagem
    ###############################################################################
    
    margem = 0.1 # minima em % do papel
    papel_escolhido = (papel[0]*(1-margem),papel[1]*(1-margem))
    #descobrir qual a oritenação da imagem
    height, width = img_in.shape
    #gira para encaixar melhor, se necessario
    if  height >= width:
        img_in = cv2.rotate(img_in, cv2.ROTATE_90_CLOCKWISE)
        height, width = img_in.shape

    #faz as razoes de proporção por altura e largura
    Razao_altura = papel_escolhido[1]/height
    Razao_largura = papel_escolhido[0]/width
    #escolhe a razão menor
    if Razao_altura < Razao_largura:
        Ratio = Razao_altura
    else: 
        Ratio = Razao_largura
    #cria as novas dimensões da imagem e redimensiona
    nova_altura = int(height*Ratio)
    nova_largura = int(width*Ratio)
    novo_tamanho_imagem = (nova_largura, nova_altura)
    img_in = cv2.resize(img_in, novo_tamanho_imagem)

    #centraliza a imagem e coloca no preview
    margem_x = int((papel[0]-papel_escolhido[0])/2)
    margem_y = int((papel[1]-papel_escolhido[1])/2)

    ###############################################################################
    #                       Processar 
    ###############################################################################

    img_contorno,lista_contorno = Gera_contornos_Vf(img_in)
    img_preenchimento,lista_preenchimento = Gera_preenchimento_Vf(img_in)
    lista_pontos = lista_contorno+lista_preenchimento
    img_in = img_contorno+img_preenchimento

    image[margem_y:nova_altura+margem_y,margem_x:nova_largura+margem_x] = img_in

    cv2.imshow('Preview', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return lista_pontos
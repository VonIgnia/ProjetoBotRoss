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
        #print (Prototipo_lista_preenchimentos)
    return Prototipo_lista_preenchimentos

def Gera_preenchimento_V3(imagem_binarizada,distancia_linha=10,grossura_linha=8):
    # Display the binary image
    #cv2.imshow('Binary Image', imagem_binarizada)
    #cv2.waitKey(0)
    
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
        
        cv2.rectangle(imagem_binarizada,(x,y),(x+w,y+h),(255,255,255),5)
        
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
    
    #cv2.imshow('Masked Image', imagem_binarizada)
    #cv2.waitKey(0)
    print (Prototipo_lista_preenchimentos)

    return Prototipo_lista_preenchimentos
 
def Gera_preenchimento_V4(imagem_binarizada):
    # Display the binary image
    cv2.imshow('Binary Image', imagem_binarizada)

    height, width = imagem_binarizada.shape[:2]
    distancia_linha = 10
    grossura_linha = 8


    imagem_linha = np.zeros(((height, width)), dtype=np.uint8)
    
    
    """
    lista_pontos = []
    for y in range(0, height, 5):
        ultimo_pixel_branco = width+100
        for x in range(0, width):
            if imagem_binarizada[y,x] == 255:
                imagem_linha[y,x] = 255
                if(ultimo_pixel_branco+1) != x:
                    #linha nova
                    lista_pontos.append([y,x])
                ultimo_pixel_branco = x
            else: #nao é branco
                if len(lista_pontos) == 0:
                    #termino da linha anterior
                    lista_pontos.append([y,x-1])
    """

    for y in range(0, height, 5):
        for x in range(0, width):
            if imagem_binarizada[y,x] == 255:
                imagem_linha[y,x] = 255
            else:
                imagem_linha[y,x] = 0
    
    # Display the binary image
    cv2.imshow('Masked Image', imagem_linha)

    """
    imagem_teste = np.zeros(((height, width)), dtype=np.uint8)
    for i in range(0,len(lista_pontos),2):
        try:
            x1 = lista_pontos[i][1]
            y1 = lista_pontos[i][0]
            x2 = lista_pontos[i+1][1]
            y2 = lista_pontos[i+1][0]
            cv2.line(imagem_teste, (x1, y1), (x2, y2), 255)
        except:
            pass
            

     # Display the binary image
    cv2.imshow('Resultado', imagem_teste)
    """
   
    cv2.waitKey(0)

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

 
img_in = cv2.imread("imgs_iniciais\shapes.jpg", cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
_, imagem_binarizada = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
point_positions = Gera_preenchimento_V5(imagem_binarizada)


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

    
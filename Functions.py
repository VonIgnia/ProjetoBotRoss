#bibliotecas necesárias para o socket
import socket
import time

#bibliotecas necessárias para os contornos
import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import *

def select_threshold(image,tipo_treshold=""):
    # Function to be called when the trackbar value changes
    def update_threshold(value):
        # Apply the threshold to obtain a binary image
        _, thresholded_image = cv2.threshold(frame, value, 255, cv2.THRESH_BINARY)
        # Display the thresholded image
        cv2.imshow(nameWindow, thresholded_image)
        selected_threshold[0] = value

    # Determine the maximum dimension of the image
    max_dim = max(image.shape[0], image.shape[1])

    # Calculate the scaling factor to fit within a 500x500 frame
    scale_factor = 500 / max_dim

    # Resize the image while preserving the aspect ratio
    resized_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)

    # Create a 500x500 frame
    frame = np.ones((500, 500), dtype=np.uint8) * 255

    # Calculate the coordinates to center the image
    x_offset = (frame.shape[1] - resized_image.shape[1]) // 2
    y_offset = (frame.shape[0] - resized_image.shape[0]) // 2

    # Insert the resized image into the frame
    frame[y_offset:y_offset+resized_image.shape[0], x_offset:x_offset+resized_image.shape[1]] = resized_image

    # Create a window to display the thresholded image
    nameWindow = "selecionar o valor do treshold para " + tipo_treshold
    cv2.namedWindow(nameWindow)

    # Create a trackbar for the threshold value
    initial_threshold = 127
    selected_threshold = [initial_threshold]  # Use a list to store the threshold value

    cv2.createTrackbar('Threshold', nameWindow, initial_threshold, 255, update_threshold)

    # Initialize with the initial threshold value
    update_threshold(initial_threshold)

    # Wait for a key press to exit
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return selected_threshold[0]

def Gera_contornos_Vf(img_in):

    treshold_value = select_threshold(img_in,"contorno")

    _, thresh = cv2.threshold(img_in, treshold_value, 255, cv2.THRESH_BINARY)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    #drop the last contourn (the frame)
    contours = contours[:-1]
    
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

def Gera_preenchimento_Vf(img_in):

    treshold_value = select_threshold(img_in,"preenchiemento")

    _, imagem_binarizada = cv2.threshold(img_in, treshold_value, 255, cv2.THRESH_BINARY_INV)

    height, width = imagem_binarizada.shape[:2]
    line_spacing = 2

    # create a frame
    image = np.zeros(imagem_binarizada.shape, dtype=np.uint8)

    # Draw horizontal lines on the binary image
    for y in range(0, height, line_spacing):
        for x in range(0, width):
            image[y,x] = imagem_binarizada[y,x]

    imagem_binarizada = image

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

def escala_imagem(img_in,papel=(297 , 210),margem=0.1):
    #imagem do preview
    image = np.zeros((500, 700), dtype=np.uint8)

    # desenhe o tamnaho das folhas na imagem
    color = (100, 100, 100)  # White color (BGR format)
    thickness = 1  # Thickness of the rectangle border
    start_point = (0, 0)  # Top-left corner of the rectangle   (148 , 105)

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
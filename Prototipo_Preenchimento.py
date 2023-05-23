
import cv2
import numpy as np
import Functions
image = cv2.imread('imgs_iniciais\kirby.png')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Apply binary thresholding
_, imagem_binarizada = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

def preenchimento(imagem_binarizada,distancia_linha=10,grossura_linha=8):
    
    # Display the binary image
    cv2.imshow('Binary Image', imagem_binarizada)

    # Set the size and separation of the lines
    height, width = imagem_binarizada.shape[:2]
    line_spacing = distancia_linha
    line_thickness = grossura_linha

    # Draw horizontal lines on the binary image
    for y in range(0, height, line_spacing):
        cv2.line(imagem_binarizada, (0, y), (width, y), 0, line_thickness)

    # Display the binary image
    cv2.imshow('Masked Image', imagem_binarizada)
    cv2.waitKey(0)
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

    Prototipo_lista_preenchimentos = []

    i_atual = 0 #flag para checar se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
    
    for i in dict_filling_points: #para cada elemento(contorno(conjunto de pontos [x, y])) no dicionário
        for j in dict_filling_points[i]: #para cada ponto[x, y] no contorno:

            j = list(np.append(j,0)) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z, esse valor sempre é 0
            if i != i_atual: #se mudou de Contorno{numero do contorno} para Contorno{numero do contorno+1}
                Prototipo_lista_preenchimentos.append(list(np.add(j,[0,0,60]))) #acrescenta movimento em Z no inicio do contorno para não rabiscar entre contornos
                i_atual = i
            Prototipo_lista_preenchimentos.append(j)

        Prototipo_lista_preenchimentos.append(list(np.add(Prototipo_lista_preenchimentos[-1],[0,0,60])))   #acrescenta movimento em Z no fim do contorno para não rabiscar entre contornos
        print(Prototipo_lista_preenchimentos)
    return Prototipo_lista_preenchimentos

#preenchimento(imagem_binarizada,10,8)

Functions.Gera_preenchimento_V3(imagem_binarizada,10,8)
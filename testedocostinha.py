
import cv2
import numpy as np

image = cv2.imread('imgs_iniciais\sonic_logo.jpg')
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
    #cv2.imshow('Masked Image', imagem_binarizada)

    # Find contours
    contours, hierarchy = cv2.findContours(imagem_binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #create a list to pass only the first and last coordinate of contourns
    #list_fillings = []
    #for i in range(len(contours)):
    #    print (list(contours[i][0][0]))
    #    
    #    list(contours[i][0][0]).append(0)
    #    print (list(contours[i][0][0]).append(0))
    #    list_fillings.append(list(np.add(contours[i][0][0],[0,0,60])))
    #    list_fillings.append(contours[i][0][0]) 
    #    list_fillings.append(contours[i][-1][0])
    #    list_fillings.append(list(np.add(contours[i][-1][0],[0,0,60])))
    
    #print(list_fillings)
    
    i=0
    #dict_filling_points = {}
    for contour in contours:
        i+=1
        print (list(contours[i][0][0]))
        
        start_filling_points = []
        filling_points = []
        for point in contour:
            print (point)
            if point == contours[i][0][0]:
                print (point)
            point = list(np.append(point,0)) #acrescentando o eixo z
            
            
            #point[0].append(0) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z
            #filling_points.append(list(np.add(point,[0,0,60])))
            filling_points.append(point)
            #filling_points.append(point[-1])
            #filling_points.append(list(np.add(point[-1],[0,0,60])))
            #print ("ponto",point[0], "do contorno:",i)
        #dict_filling_points["Contorno{}".format(i)] = filling_points
   #print(filling_points)

    # Convert the grayscale image to color
    #image = cv2.cvtColor(imagem_binarizada, cv2.COLOR_GRAY2BGR)

    # Draw interior contours in red
    #for i in range(len(contours)):
    #    if hierarchy[0][i][3] != -1:
    #        cv2.drawContours(image, contours, i, (0, 0, 255), 2)

    # Display the image with contours
    #cv2.imshow('Image with Contours', image)

    # Wait for a key press and then close the window
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return

preenchimento(imagem_binarizada,10,8)
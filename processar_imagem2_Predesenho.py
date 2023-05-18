import cv2
import numpy as np


image = cv2.imread('kirby.png', cv2.IMREAD_GRAYSCALE)



cv2.imshow('Grayscale Image', image)

# Apply Canny edge detection
edges = cv2.Canny(image, threshold1=100, threshold2=200, apertureSize=3)

# Display the edges
cv2.imshow('Canny Edges', edges)

# Apply thresholding to obtain a binary image
_, threshold = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY)

# Find contours
contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Draw contours on the original image
image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

#Define initial contour
initial = 2

#Define minimum length
minimum_length = 25

contour_points = []
#FASDFASDFASDF

# Draw interior contours in red
contour_number = 0
dict_contour_points = {}
for i in range(initial,len(contours)):
    if hierarchy[0][i][3] != -1:
        perimeter = cv2.arcLength(contours[i],True)

        #Draw contours with at least the minimum length
        if perimeter >= minimum_length:

            #Draw contours starting at initial count
            if contour_number >= initial:
                cv2.drawContours(image, contours, i, (0, 0, 255), 1)

                contour_points = []
    
                # o loop "for" a seguir tem como objetivo salvar os pontos de cada contorno detectado, separadamente uns dos outros,
                #assim permitindo chamar os contornos separadamente
                for point in contours[i]:
                    #point[0].append(0) # a lista só contém os valores de x e y, essa linha faz o append de um terceiro valor para representar o eixo z
                    contour_points.append(point[0])
                    #print ("ponto",point[0], "do contorno:",i)
                    print(len(contours[i]))
                
                dict_contour_points["Contorno{}".format(i)] = contour_points
                print(i)
                break
            contour_number += 1

# Display the image with contours
cv2.imshow('Image with Contours', image)

#print (dict_contour_points)

cv2.waitKey(0)
cv2.destroyAllWindows()
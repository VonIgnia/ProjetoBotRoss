import cv2
from pykuwahara import kuwahara

image = cv2.imread('imgs_avancadas\Lenna.png')

filt1 = kuwahara(image, method='mean', radius=3)
#filt2 = kuwahara(image, method='gaussian', radius=7, sigma=1.5)    # default sigma: computed by OpenCV
filt2 = kuwahara(image, method='gaussian', radius=5)    # default sigma: computed by OpenCV

#cv2.imwrite('lena-kfilt-mean.jpg', filt1)
cv2.imwrite('lena-kfilt-gaus.jpg', filt2)
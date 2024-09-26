import cv2
import numpy as np
import matplotlib.pyplot as plt
code_img = cv2.imread("EclipseStreamAnalysis/capturedFrames/frame1.png", 0)
print("Non Zero count, unfiltered, cv2: ",cv2.countNonZero(code_img))#28,000

from PIL import Image  
from numpy import asarray  
# loading the Image and converting it into  
# numpy array  
img = Image.open("EclipseStreamAnalysis/capturedFrames/frame1.png")  
numpydata = asarray(img)   
# data  
print("Number of non zero pixels: ",np.count_nonzero(numpydata))
imgplot = plt.imshow(numpydata)
plt.show()

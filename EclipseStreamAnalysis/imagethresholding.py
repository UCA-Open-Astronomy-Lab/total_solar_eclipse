"""
 * Python script to demonstrate simple thresholding.
 *
 * usage: python Threshold.py <filename> <sigma> <threshold>
"""
import numpy as np
import skimage.color
import skimage.filters
import skimage.io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#test
# get filename, sigma, and threshold value from command line
filename = "EclipseStreamAnalysis/frame1.png"
sigma = float(1.0) #controls how "Blurred" an image is, lower is clearer
t = float(1.0)#Base threshold value
t_rescaled = 0.95 #rescaled thrshold value gathered from grayscale.py

# read and display the original image
image = mpimg.imread(filename)
imgplot = plt.imshow(image)

# blur and grayscale before thresholding
blur = skimage.color.rgb2gray(image)
blur = skimage.filters.gaussian(blur, sigma=2)

# perform inverse binary thresholding
mask = blur > t_rescaled #it is greater than because we want white pixels

# use the mask to select the "interesting" part of the image
sel = np.zeros_like(image)
sel[mask] = image[mask]

# display the result
imgplot = plt.imshow(sel)
#plt.show()

sum = 0
for i in range(len(sel[0:,0,0])):
    for j in range(len(sel[0,0:,0])):
        for k in range(len(sel[0,0,0:])):
            if sel[i,j,k] > 0:
                sum += 1
                break
print(sum)

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

#setting up test storage for pixel count info inital date = 2460409.2186657293
SecondToJD = 1.1574e-5
t0 = 2460409.2186657293
time = []#time in julian date of each pixel count
pixelcount = []#pixelcount of frame with mask

#sigma, and threshold value
sigma = float(1.0) #controls how "Blurred" an image is, lower is clearer
t = float(1.0)#Base threshold value
t_rescaled = 0.95 #rescaled thrshold value gathered from grayscale.py

for l in range(1,21):
    #get filename
    filename = "EclipseStreamAnalysis/capturedFrames/frame"+str(l)+".png"

    # read and display the original image
    image = mpimg.imread(filename)

    # blur and grayscale before thresholding
    blur = skimage.color.rgb2gray(image)
    blur = skimage.filters.gaussian(blur, sigma=2)

    # perform inverse binary thresholding
    mask = blur > t_rescaled #it is greater than because we want white pixels

    # use the mask to select the "interesting" part of the image
    sel = np.zeros_like(image)
    sel[mask] = image[mask]

    #count pixels
    sum = 0
    for i in range(len(sel[0:,0,0])):
        for j in range(len(sel[0,0:,0])):
            for k in range(len(sel[0,0,0:])):
                if sel[i,j,k] > 0:
                    sum += 1
                    break
    print(l, ": ",sum)
    pixelcount.append(sum)
    time.append(t0 + (l-1)*SecondToJD)

plt.plot(time, pixelcount, label = "Pixel Count")
plt.title("2024-04-08 Total Solar Eclipse, Conway, AR 1429.25 MHz")
plt.xlabel('JD Time')
plt.ylabel('# of Pixels >= 0.95')
plt.show()
"""
#get filename
filename = "EclipseStreamAnalysis/capturedFrames/frame"+str(1)+".png"

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

#count pixels
sum = 0
for i in range(len(sel[0:,0,0])):
    for j in range(len(sel[0,0:,0])):
        for k in range(len(sel[0,0,0:])):
            if sel[i,j,k] > 0:
                sum += 1
                break
print(sum)"""


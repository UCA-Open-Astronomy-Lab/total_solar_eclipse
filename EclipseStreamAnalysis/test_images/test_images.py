import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# A block of 12 white pixels
print("Testing a block of 12 white pixels")
img = cv.imread('64x64_12_white_pixels_block.png', cv.IMREAD_GRAYSCALE)
nonzero_pixel_count = np.sum(img > 0)
print("Number of nonzero pixels (should be 12): ", nonzero_pixel_count)

# 12 whie pixels scattered around
print("Testing 12 individual white pixels")
img = cv.imread('64x64_12_individual_white_pixels.png', cv.IMREAD_GRAYSCALE)
nonzero_pixel_count = np.sum(img > 0)
print("Number of nonzero pixels (should be 12): ", nonzero_pixel_count)

# 12 whie pixels in a group
print("Testing 12 grouped white pixels")
img = cv.imread('64x64_12_grouped_white_pixels.png', cv.IMREAD_GRAYSCALE)
nonzero_pixel_count = np.sum(img > 0)
print("Number of nonzero pixels (should be 12): ", nonzero_pixel_count)

# A fuzzy ball of 36 nonzero pixels
print("Testing blurry ball of 36 nonzero pixels")
img = cv.imread('64x64_36_nonzero_pixels_blur.png', cv.IMREAD_GRAYSCALE)
nonzero_pixel_count = np.sum(img > 0)
print("Number of nonzero pixels (should be 36): ", nonzero_pixel_count)

# Real image from the eclipse
print("Testing a real image from the eclipse")
img = cv.imread('64x64_eclipse.png', cv.IMREAD_GRAYSCALE)
nonzero_pixel_count = np.sum(img > 0)
print("Number of nonzero pixels:", nonzero_pixel_count)

# 64x64 chunk of a real image from the eclipse, manual thresholding
print("Testing a real image from the eclipse, manual thresholding")
img = cv.imread('64x64_eclipse.png', cv.IMREAD_GRAYSCALE)
nonzero_pixel_count = np.sum(img > 127)
print("Number of nonzero pixels:", nonzero_pixel_count)

# 64x64 chunk of a real image from the eclipse, openCV thresholding
print("Testing a real image from the eclipse, global thresholding using openCV")
img = cv.imread('64x64_eclipse.png', cv.IMREAD_GRAYSCALE)
ret,thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
nonzero_pixel_count = np.sum(thresh1 > 0)
print("Number of nonzero pixels:", nonzero_pixel_count)

# Full eclipse image, openCV thresholding
print("Testing a real image from the eclipse, global thresholding using openCV")
img = cv.imread('frame1.png', cv.IMREAD_GRAYSCALE)
ret,thresh1 = cv.threshold(img, 242, 255, cv.THRESH_BINARY)
nonzero_pixel_count = np.sum(thresh1 > 0)
print("Number of nonzero pixels:", nonzero_pixel_count)

# Graphical look at what's going on
titles = ["Original Image", "OpenCV, Binary thresholding"]
images = [img, thresh1]

for i in range(2):
    plt.subplot(1,2,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
 
plt.savefig('openCV_thresholding.png')


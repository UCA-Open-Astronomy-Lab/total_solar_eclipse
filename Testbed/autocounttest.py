import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import ffmpeg
import datetime
import os

#Testing 
#t_0 = 1:56:50
#t_f = 1:57:10

eclipse_mp4 = "EclipseStreamAnalysis/2024 April 8, 4k Live Stream of the Solar Eclipse from the UCA Observatory [lrWkmZvI3JY].mp4"
start_time = "00:00:00"
totality_start_time = "01:57:26"
totality_end_time = "02:01:22"
end_time = "03:18:47"
crop_dimensions = '1300:1300:1300:500' #sets values for cropping, from left to right: Width of cropped video, height of cropped video, top left x coordinate of cropped video, top left y coordinate for cropped video

#setting up test storage for pixel count info inital date = 2460409.2186657293
SecondToJD = 1.1574e-5
t0 = 2460409.2186657293
time = []#time in julian date of each pixel count
pixelcount = []#pixelcount of frame with mask

for i in range(3*60):
    starttimeindex = str(datetime.timedelta(seconds = i*60))
    endtimeindex = str(datetime.timedelta(seconds = i*60+1))
    (
        ffmpeg.input(eclipse_mp4, ss=starttimeindex, to=endtimeindex)#the video we want to extract data from
        .filter('crop', *crop_dimensions.split(":"))#crops the video
        .filter('fps', fps=1, round='up')
        .output('Testbed/FrameStore/countframe.png')# extracts frames and saves them as pngs
        .run()
    )
    
    filename = "Testbed/FrameStore/countframe.png"
    img = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    
    #thresh = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       #   cv.THRESH_BINARY, 199, 5) 
    #thresh = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, 
                                        #  cv.THRESH_BINARY, 199, 5) 

    ret, thresh = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    nonzero_pixel_count = np.sum(thresh > 0)
    pixelcount.append(nonzero_pixel_count)
    time.append(t0 + (i)*SecondToJD)
    os.remove('Testbed/FrameStore/countframe.png')

plt.plot(time, pixelcount, label = "Pixel Count")
plt.title("2024-04-08 Total Solar Eclipse, Conway, AR 1429.25 MHz")
plt.xlabel('JD Time')
plt.ylabel('# of Pixels')
plt.show()

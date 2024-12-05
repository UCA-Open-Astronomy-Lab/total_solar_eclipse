from PIL import Image
import pytesseract
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import ffmpeg
import datetime 
import os
import csv
import pandas as pd


eclipse_mp4 = "EclipseStreamAnalysis/2024 April 8, 4k Live Stream of the Solar Eclipse from the UCA Observatory [lrWkmZvI3JY].mp4"
pixel_crop_dimensions = '1300:1300:1300:500' #sets values for cropping, from left to right: Width of cropped video, height of cropped video, top left x coordinate of cropped video, top left y coordinate for cropped video
time_crop_dimensions = '600:110:1630:2030' #sets values for cropping, from left to right: Width of cropped video, height of cropped video, top left x coordinate of cropped video, top left y coordinate for cropped video

#setting up test storage for pixel count info inital date = 2460409.2186657293
SecondToJD = 1.1574e-5 #Conversion factor for seconds to julian date
t0 = 2460409.2036806#2460409.20369213#2460409.162013889#This is the real start date based on the time of the video #2460409.2036806
videotime = []#time in julian date of each pixel count using the formula i originally used
clocktime = []#the time from the clock in the video
pixelcount = []#pixelcount of frame with mask
timestring = []

for i in range(3*60+18+1): #keep in mind what j value you choose, as you will have to modulate in responce. Can be seconds or minutes
    j = i*60 #change this value if you want to look at different time jumps. j = i is seconds, j = 60*i is minutes etc
    starttimeindex = str(datetime.timedelta(seconds = 46+j))
    endtimeindex = str(datetime.timedelta(seconds = 46+j+1))
    (
        ffmpeg.input(eclipse_mp4, ss=starttimeindex, to=endtimeindex)#the video we want to extract data from
        .filter('crop', *pixel_crop_dimensions.split(":"))#crops the video
        .filter('fps', fps=1, round='up')
        .output('Time Test/timeframe test/countframe.png')# extracts frames and saves them as pngs
        .run()
    )
    (
        ffmpeg.input(eclipse_mp4, ss=starttimeindex, to=endtimeindex)#the video we want to extract data from
        .filter('crop', *time_crop_dimensions.split(":"))#crops the video
        .filter('fps', fps=1, round='up')
        .output('Time Test/timeframe test/timeframe.png')# extracts frames and saves them as pngs
        .run()
    )
    
    """Pixel Counting"""
    filename = "Time Test/timeframe test/countframe.png"
    img = cv.imread(filename, cv.IMREAD_GRAYSCALE) #reads the image file and converts to grayscale
    ret, thresh = cv.threshold(img, 0, 255, cv.THRESH_OTSU)#Otsu threholding
    nonzero_pixel_count = np.sum(thresh > 0) #counts nonzero pixels of the thresholded image matrix
    pixelcount.append(nonzero_pixel_count) #adds the pixel count to a list to display as a graph
    videotime.append(t0 + (j)*SecondToJD) #counts the time #####################OLD METHOD###########################
    os.remove('Time Test/timeframe test/countframe.png')

    """Optical Character Recognition"""
    filename = 'Time Test/timeframe test/timeframe.png'
    img1 = np.array(Image.open(filename))#turnsimage into array
    time = pytesseract.image_to_string(img1)#tesseract views image and finds characters
    print("Time Before Editing: ", time)
    if(time[1] == ':'): #adds a 0 in front of numbers after 12
        time = "0"+time
    if (time[1] == '7' or time[1] == '5'):#takes care of error where tesseract mistakes leading 1 and 2 for a 7
        time = error1 + time[2:8]
    if(time[0] == ':'): #takes care of error where tesseract misses the first two numbers, leaving a ':' as first char
        time = error1+time
    if(time[2] != ':'):
         time = error1+":"+time[3:8]
    if(time[3] == ':'):
         time = time[0:3]+error2+time[5:8]
    if(time[5] != ':'):
         time = time[0:5]+':'+error3
    if(time[0] == '0'):#converts to 24h time
        time = str(12+int(time[1]))+time[2:8]

    time = time[:8]#cuts down time string to '00:00:00' format
    timestring.append(time)

    with open('Time Test/timeframe test/clocktime.csv', 'w') as f:#saves timestring to csv to view any errors
            writer = csv.writer(f)
            writer.writerows((timestring))

    print("time post editing:", time)

    CST = datetime.datetime.fromisoformat('2024-04-08T'+time)#converts to date format
    ts = datetime.datetime.timestamp(CST)
    UTC = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)#converts to utc

    pdts = pd.Timestamp(UTC)#converts to timestamp for julian date conversion
    jd = pdts.to_julian_date()#converts to julian date
    print("time:,", time)
    print("CST: ",CST)
    print("UTC: ",UTC)
    print("Julian Date: ",jd)

    error1 = time[0:2]# saves first two characters to fix errors above with
    error2 = str(int(time[3:5])+1)
    error3 = str(int(time[6:8])+1)

    clocktime.append(jd)
    os.remove('Time Test/timeframe test/timeframe.png')

with open('Time Test/timeframe test/clockjd.csv', 'w') as f:#saves timestring to csv to view any errors
        writer = csv.writer(f)
        writer.writerow((clocktime))

with open('data/PixelCount.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows((pixelcount, videotime))

"""
with open('data/PixelCount.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows((pixelcount, videotime))"""

#plt.plot(videotime, pixelcount, label = "Pixel Count")
plt.plot(videotime, label = "Video Time")
plt.plot(clocktime, label = "Clock Time")
plt.legend()
plt.title("Comparison of clock time and video time")
plt.ylabel('JD Time')
plt.xlabel('Frame #')
plt.show()
'''
"""Graphs Data"""
plt.plot(date, r_pol + adjustment_function, label = "Adjusted Radio Data")#adjusted Graph
plt.axvline(x = date[index_1st], color = 'r', linestyle = '-') #1st contact
plt.axvline(x = date[index_2nd], color = 'r', linestyle = '-') #2nd contact
plt.axvline(x = date[index_3rd], color = 'r', linestyle = '-') #3rd contact
plt.axvline(x = date[index_4th], color = 'r', linestyle = '-') #4th contact
plt.title("2024-04-08 Total Solar Eclipse, Conway, AR 1429.25 MHz")
plt.xlabel('JD Time')
plt.ylabel('%\ of total')
plt.legend()
plt.savefig("RadioVisualComparison.png")
plt.show()
'''
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import ffmpeg
import datetime
import os
import pandas as pd
import csv
import pytesseract
from PIL import Image
import datetime 




#setting up test storage for pixel count info inital date = 2460409.2186657293
SecondToJD = 1.1574e-5 #Conversion factor for seconds to julian date
t0 = 2460409.162013889#This is the real start date based on the time of the video #2460409.2036806
time = []#time in julian date


'''
According to this website, https://apps.aavso.org/v2/tools/julian-date-converter/

11:53:18 CDT Real Start Time of Video, 2024-04-08 15:53:18 UTC = 2460409.162013889
12:53:18 CDT target, 16:53:18 UTC, 2024-04-08 16:53:18 UTC = 2460409.2036805553, 
15:12:23 CDT real end time of video, 2024-04-08 20:12:23 UTC = 2460409.3419328704

//radio telescope begin and end date
2460409.2186657293 = 2024-04-08 17:14:52.719 time radio observations started, 12:14:52.719 PM
2460409.3424835186 = 2024-04-08 20:13:10.576 time radio observation ended, 03:13:10.576 PM

beginning of video at 00:00:00, time is 11:53:18 CDT
beginning of video at 01:00:00, time is 12:53:36 CDT

in the span of an hour, it was off by 18 seconds.
if this continues for the rest of the time, then the final time will be off by 59.6 seconds



//frames
29.97 fps
frames after 1 hour: 107,892

30.00 fps
frames after 1 hour: 108,000
'''
'''
time_clock = 2460409.2036805553#JD at 1 hour into the video based on the clock
time_calc = time[60]#JD at 1 hour based on the calculator
daytosec = 24*60*60
frames = 3*60+18
time_error = (time_clock-time_calc)#over the hour
'''


'''This part of the code will test to see which frames starts the first whole second of the video

for 29.97, frame 8 is the first frame of a first second on 11:53:19 CDT
for 30.00, frame 8 is the first frame of a first second on 11:53:19 CDT
'''
eclipse_mp4 = "EclipseStreamAnalysis/2024 April 8, 4k Live Stream of the Solar Eclipse from the UCA Observatory [lrWkmZvI3JY].mp4"
start_time = "00:00:00"
crop_dimensions = '500:110:1630:2030' #sets values for cropping, from left to right: Width of cropped video, height of cropped video, top left x coordinate of cropped video, top left y coordinate for cropped video
clocktime = []

#figur eout how to look at a specific frame
#t_0: 11:53:18
#t_1: 12:53:36
#t_2: 01:53:36
#t_3: 02:53:36
for i in range(3*60+18): #keep in mind what j value you choose, as you will have to modulate in responce. Can be seconds or minutes
    j = i*60 #change this value if you want to look at different time jumps. j = i is seconds, j = 60*i is minutes etc
    starttimeindex = str(datetime.timedelta(seconds = j))
    endtimeindex = str(datetime.timedelta(seconds = j+1))

    (
        ffmpeg.input(eclipse_mp4, starttimeindex, endtimeindex)#the video we want to extract data from
        .filter('crop', *crop_dimensions.split(":"))#crops the video
        .filter('fps', fps=1)
        .output('Time Test/timeframe test/frame1.png')# extracts frames and saves them as pngs
        .run()
    )
    filename = 'Time Test/timeframe test/frame1.png'
    img1 = np.array(Image.open(filename))
    time = pytesseract.image_to_string(img1)

    if(time[1] == ':'):
        time = "0"+time
    time = time[:8]
    print("time:", time)

    CST = datetime.datetime.fromisoformat('2024-04-08T'+time)
    ts = datetime.datetime.timestamp(CST)
    UTC = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)

    pdts = pd.Timestamp(UTC)
    jd = pdts.to_julian_date()
    print("time:,", time)
    print("CST: ",CST)
    print("UTC: ",UTC)
    print("Julian Date: ",jd)
    
    clocktime.append(jd)
    os.remove('Time Test/timeframe test/frame1.png')






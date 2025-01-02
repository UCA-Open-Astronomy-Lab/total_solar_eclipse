from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astropy.time import Time
from matplotlib import dates
import numpy as np
import pandas as pd
import csv
import scipy.signal
import datetime 
#from sqlalchemy import null

"""Data from the fits file"""
hdu1 = fits.open("../data/20240408-171452_TPI-PROJ01-SUN_02#_01#.fits")
data = hdu1[1].data
t = Time(data['jd'], format='jd')
date = data['jd']
t = t.plot_date
r_pol = data['RIGHT_POL']
#len date 9935

"""code used to find the indexes of the 1-4 contact"""

#These times were found with an online calculator using uca's posted eclipse times
contact1st = 2460409.231829
contact2nd = 2460409.285475
contact3rd = 2460409.288160
contact4th = 2460409.341400

#These times were found just using math and python lists
final = date[-1]
pre1st = contact1st - (final - contact4th)

#these are the indexes of each of the times above in the date[] list
index_pre = 0
index_1st = 0
index_2nd = 0
index_3rd = 0
index_4th = 0
index_final = 0
epsilon = 1e-6 #Tolerance

#"""Finds pre1st contact index"""
for i in range(len(date)):
    if (pre1st - date[i]) < epsilon:
        index_pre = i
        #print("found pre1st index", index_pre)
        break

#"""Finds 1st contact index"""
for i in range(len(date)):
    if (contact1st - date[i]) < epsilon:
        index_1st = i
        #print("found 1st index", index_1st)
        break

#"""Finds 2nd contact index"""
for i in range(len(date)):
    if (contact2nd - date[i]) < epsilon:
        index_2nd = i
        #print("found 2nd index", index_2nd)
        break

#"""Finds 3rd contact index"""
for i in range(len(date)):
    if (contact3rd - date[i]) < epsilon:
        index_3rd = i
        #print("found 3rd index", index_3rd)
        break

#"""Finds 4th contact index"""
for i in range(len(date)):
    if (contact4th - date[i]) < epsilon:
        index_4th = i
        #print("found 4th index", index_4th)
        break

#"""Finds final data index"""
for i in range(len(date)):
    if (final - date[i]) < epsilon:
        index_final = i
        #print("found final index", index_final)
        break

"""Code to calculate line of adjustment"""
#calculates average magnitude of the amount of time before 1st contact that is available post 4th contact
sum = 0
dif = index_1st - index_pre
for i in range(index_pre, index_1st):
    sum = sum + r_pol[i]
pre_average = sum/dif
#print(pre_average)

#calculates average magnitude after 4th contact
sum = 0
dif = index_final - index_4th
for i in range(index_4th, index_final):
    sum = sum + r_pol[i]
post_average = sum/dif
#print(post_average)

#calculates how much the last values in the data need to be adjusted
adj_num = pre_average - post_average

#Creates the linear adjustment function
m = adj_num/(date[-1]- date[index_1st])
adjustment_function = []

#This part sets the part of the function from 0 to 1st contact to 0 as to not effect that first part with the adjustment function.
for i in range(0, index_1st):
    adjustment_function.append(0)

#This part is the adjustment function, which affects the data from 1st contact to the last point of data.
for i in range(index_1st, index_final+1):
    adjustment_function.append(m*(date[i]- date[index_1st]))

"""Making Visual Data counts into percentage"""
def read_lines():
    with open('../data/PixelCount.csv', 'rU') as data:
        reader = csv.reader(data)
        for row in reader:
            yield [ float(i) for i in row ]

#time and count lists
xy = list(read_lines())
count = xy[0][:]
time = xy[1][:]

def read_lines2():
    with open('../Time Test/timeframe test/clockjd.csv', 'rU') as data:
        reader = csv.reader(data)
        for row in reader:
            yield [ float(i) for i in row ]
x = list(read_lines2())
clocktime = x[0][:]

cti1 = 0
cti2 = 0
cti3 = 0
cti4 = 0
error1 = 1
error2 = 1

for i in range(len(count)):
    if(count[i] == 91537):#cuts out the no signal section
        count[i] = None
    if(abs(contact2nd - clocktime[i]) <= error1):
        error1 = abs(clocktime[i] - contact2nd)
        cti1 =i
    if(abs(clocktime[i] - contact3rd) <= error2):
        error2 = abs(clocktime[i] - contact3rd)
        cti2 = i
for i in range(cti1, cti2):
    count[i] = None
for i in range(1):
    count[i] = None

'''Converting Livestream data to percentage'''
#finds average value of first ten counts pre eclipse
sum = 0
for i in range(1,11):
    sum += count[i]
topaverage = sum/10

percentcount = np.array(count)
for i in range(len(count)):
    if(percentcount[i] != None):
        percentcount[i] = (percentcount[i]*100)/topaverage
percentcount = percentcount.tolist()


'''Normalizing and smoothing Radio Data'''
r_pol_filter = scipy.signal.savgol_filter(r_pol + adjustment_function, 51, 0) #smoothed radio data

def normalization(lightcurve):
    high = 0
    for i in range(len(lightcurve)):
        if (lightcurve[i] >= high):
            high = lightcurve[i]

    n = high/100

    return lightcurve/n

normalSmooth_r_pol_filter = scipy.signal.savgol_filter(normalization(r_pol + adjustment_function), 51, 0)


'''Light Sensor Data'''
# Read the CSV file into a DataFrame
df = pd.read_csv("../data/light_sensor.csv")

time_sensor = df["Run 2: Time (h)"]
illumination_sensor = df["Run 2: Illumination (lux)"]

normal_illumination_sensor = normalization(illumination_sensor)

time_sensor = time_sensor.values.tolist()
jd_sensor = []

for i in range(len(time_sensor)):
    CST = datetime.datetime.fromisoformat('2024-04-08T'+time_sensor[i])
    ts = datetime.datetime.timestamp(CST)
    UTC = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)

    pdts = pd.Timestamp(UTC)
    jd = pdts.to_julian_date()
    jd_sensor.append(jd)



# Adding the Stellarium data

stellarium_lightcurve = np.genfromtxt("../Stellarium/stellarium_lightcurve.csv", delimiter=",")

# Adding the theoretical models

str2date = lambda x: pd.Timestamp(datetime.datetime.fromtimestamp(datetime.datetime.timestamp(datetime.datetime.fromisoformat(x)), datetime.timezone.utc)).to_julian_date()
rsun_1p00 = np.genfromtxt("../EclipseModels/tse_radius_1.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p05 = np.genfromtxt("../EclipseModels/tse_radius_1.05.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p10 = np.genfromtxt("../EclipseModels/tse_radius_1.1.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p15 = np.genfromtxt("../EclipseModels/tse_radius_1.15.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p20 = np.genfromtxt("../EclipseModels/tse_radius_1.2.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p25 = np.genfromtxt("../EclipseModels/tse_radius_1.25.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p27 = np.genfromtxt("../EclipseModels/tse_radius_1.27.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p30 = np.genfromtxt("../EclipseModels/tse_radius_1.3.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p35 = np.genfromtxt("../EclipseModels/tse_radius_1.35.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p40 = np.genfromtxt("../EclipseModels/tse_radius_1.4.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")
rsun_1p45 = np.genfromtxt("../EclipseModels/tse_radius_1.45.csv", delimiter=",", converters = {0: str2date}, encoding="utf-8")


"""Ratios For Data Conservation"""
'''
def dataRatio(lightcurve):
    high = 0
    for i in range(len(lightcurve)):
        if (lightcurve[i] >= high):
            high = lightcurve[i]

    low = 100
    for i in range(len(lightcurve)):
        if (lightcurve[i] <= low):
            low = lightcurve[i]
    
    return high/low
print("Baseline Radio (Tracking Error Adjustment Only): ",dataRatio(r_pol + adjustment_function))
print("Smoothed Baseline Radio (Tracking Error Adjustment + Smoothed): ",dataRatio(r_pol_filter))
print("Smoothed Adjusted - 6.372(sensor error) Ratio: ",dataRatio(r_pol_filter - rpolerror))
print("Smooth/Normal Ratio: ",dataRatio(normalization(r_pol_filter)))
print("Normal/Smooth Ratio: ",dataRatio(normalSmooth_r_pol_filter))
'''
'''
low = 100
for i in range(len(r_pol)):
    if (normalization(r_pol_filter)[i] <= low):
        low = normalization(r_pol_filter)[i]
    

print("Radio Obscuration Minimum: ",low)
'''
"""Graphs Data"""
'''colors: green, black, orange, blue, red '''


plt.figure(figsize=(12, 8)) 
widthline = 2

#Radio Telescope Plots
#Frame 1: raw
#plt.plot(date, r_pol, label = "Raw Radio Data", color = 'Green', linewidth=widthline)#RADIO raw

#Frame 2: raw, adjustment function
#plt.plot(date, r_pol, label = "Raw Radio Data", color = 'Green', linewidth=widthline)#RADIO raw
#plt.plot(date, adjustment_function, label = "Tracking Adjustment Function", linewidth=widthline)#RADIO raw

#Frame 3: adjusted radio data
#plt.plot(date, r_pol + adjustment_function, label = "Adjusted Radio Data", color = 'Green', linewidth=widthline)#RADIO raw

#Frame 4: Smoothed
#plt.plot(date, r_pol_filter, label = "Smoothed Radio Data", color = 'Green', linewidth=widthline)#RADIO Smoothed/Normalization

#Frame 5: Smoothed/Normalized


#Light Sensor Plots
#plt.plot(jd_sensor, normal_illumination_sensor, label = "Light Sensor Lightcurve (Normalized)", linewidth=widthline)#Light Sensor Visible Data

#Stellarium Theoretical Plots
#plt.plot(stellarium_lightcurve[:,0], 100-stellarium_lightcurve[:,1], label = "Theoretical Lightcurve (Stellarium)", color = "orange", linewidth=widthline)#Stellarium Data

#Livestream Plots
#plt.plot(clocktime, percentcount, label = "Livestream Lightcurve (Normalized)", color = "blue", linewidth=widthline/2)#Visual Data

#"Real" theoretical lightcurve
plt.plot(date, normalization(r_pol_filter), label = "Smoothed/Normalized Radio Data", color = 'Green', linewidth=3)#RADIO Smoothed/Normalization
plt.plot(rsun_1p30[:,0], 100*rsun_1p30[:,1], label = "R/Rsun = 1.30", linewidth=widthline)
plt.plot(rsun_1p27[:,0], 100*rsun_1p27[:,1], label = "R/Rsun = 1.27", linewidth=widthline)
plt.plot(rsun_1p25[:,0], 100*rsun_1p25[:,1], label = "R/Rsun = 1.25", linewidth=widthline)
plt.plot(rsun_1p20[:,0], 100*rsun_1p20[:,1], label = "R/Rsun = 1.20", linewidth=widthline)
plt.plot(rsun_1p10[:,0], 100*rsun_1p10[:,1], label = "R/Rsun = 1.10", linewidth=widthline)
plt.plot(rsun_1p00[:,0], 100*rsun_1p00[:,1], label = "R/Rsun = 1.0", linewidth=widthline)
#plt.plot(rsun_1p05[:,0], 100*rsun_1p05[:,1], label = "R/Rsun = 1.05", linewidth=widthline)

#plt.plot(rsun_1p15[:,0], 100*rsun_1p15[:,1], label = "R/Rsun = 1.15", linewidth=widthline)




#plt.plot(rsun_1p35[:,0], 100*rsun_1p35[:,1], label = "R/Rsun = 1.35", linewidth=widthline)
#plt.plot(rsun_1p40[:,0], 100*rsun_1p40[:,1], label = "R/Rsun = 1.40", linewidth=widthline)
#plt.plot(rsun_1p45[:,0], 100*rsun_1p45[:,1], label = "R/Rsun = 1.45", linewidth=widthline)



plt.axvline(x = date[index_1st], color = 'r', linestyle = '-') #1st contact
plt.axvline(x = date[index_2nd], color = 'r', linestyle = '-') #2nd contact
plt.axvline(x = date[index_3rd], color = 'r', linestyle = '-') #3rd contact
plt.axvline(x = date[index_4th], color = 'r', linestyle = '-') #4th contact

#Design
titlesize = 35
labelsize = 25
ticksize = 20
legendsize = 14

plt.title("Radio Lightcurve Fitting", fontsize = titlesize)
plt.xlabel('Julian Date', fontsize = labelsize)
plt.ylabel('Relative Brightness', fontsize = labelsize)
plt.xticks(fontsize = ticksize)
plt.yticks(fontsize = ticksize)
plt.ylim(-5,120)
plt.xlim(2460409.16,2460409.39)
plt.legend(fontsize = legendsize, frameon=False, loc='lower left')
plt.savefig("RadioRadiusComparison.png")
plt.show()

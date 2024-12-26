from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.time import Time
from matplotlib import dates
import numpy as np
import pandas as pd
import csv
import scipy.signal
import datetime 
from sqlalchemy import null

"""Data from the fits file"""
hdu1 = fits.open("data/20240408-171452_TPI-PROJ01-SUN_02#_01#.fits")
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
    with open('data/PixelCount.csv', 'rU') as data:
        reader = csv.reader(data)
        for row in reader:
            yield [ float(i) for i in row ]

#time and count lists
xy = list(read_lines())
count = xy[0][:]
time = xy[1][:]

def read_lines2():
    with open('Time Test/timeframe test/clockjd.csv', 'rU') as data:
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


#makes the data out of 100%
sum = 0
for i in range(1,11):
    sum += count[i]
topaverage = sum/10

percentcount = np.array(count)
for i in range(len(count)):
    if(percentcount[i] != None):
        percentcount[i] = (percentcount[i]*100)/topaverage
percentcount = percentcount.tolist()

r_pol_filter = scipy.signal.savgol_filter(r_pol + adjustment_function, 51, 0) #smoothed radio data

rpolerror = 6.372 #found the highest point above 100 and subtracted it from the rest

'''Light Sensor Data'''
# Read the CSV file into a DataFrame
df = pd.read_csv("data/light_sensor.csv")

time_sensor = df["Run 2: Time (h)"]
illumination_sensor = df["Run 2: Illumination (lux)"]/1080
uvb_sensor = df["Run 2: UVB Intensity (mW/m²)"]/6.3
uva_sensor = df["Run 2: UVA Intensity (mW/m²)"]/108

time_sensor = time_sensor.values.tolist()
illumination_sensor = illumination_sensor.values.tolist()
uvb_sensor = uvb_sensor.values.tolist()
uva_sensor = uva_sensor.values.tolist()
jd_sensor = []

for i in range(len(time_sensor)):
    CST = datetime.datetime.fromisoformat('2024-04-08T'+time_sensor[i])
    ts = datetime.datetime.timestamp(CST)
    UTC = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)

    pdts = pd.Timestamp(UTC)
    jd = pdts.to_julian_date()
    jd_sensor.append(jd)








"""Graphs Data"""
#Light Sensor Plots
'''plt.plot(jd_sensor, illumination_sensor, label = "Light Sensor Illumination")#Radio Data
plt.plot(jd_sensor, uvb_sensor, label = "Light Sensor UVB")#Radio Data
plt.plot(jd_sensor, uva_sensor, label = "Light Sensor UVA")#Radio Data
'''
radio_min = 100
for i in range(len(r_pol_filter)):
    if (r_pol_filter[i] - rpolerror) < radio_min:
        radio_min = r_pol_filter[i] - rpolerror

print('Radio Minimum: ', radio_min)
print('Visual Minimum: ', 0)



plt.plot(date, r_pol_filter - rpolerror, label = "Adjusted Radio Data")#Radio Data
plt.plot(clocktime, percentcount, label = "Adjusted Visual Data", color = "black")#Visual Data
plt.axvline(x = date[index_1st], color = 'r', linestyle = '-') #1st contact
plt.axvline(x = date[index_2nd], color = 'r', linestyle = '-') #2nd contact
plt.axvline(x = date[index_3rd], color = 'r', linestyle = '-') #3rd contact
plt.axvline(x = date[index_4th], color = 'r', linestyle = '-') #4th contact
plt.title("Radio vs Visual Data")
plt.xlabel('JD Time')
plt.ylabel('%\ of total')
plt.legend()
plt.savefig("RadioVisualComparison.png")
plt.show()
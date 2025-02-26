

import math
import matplotlib.pyplot as plt
from matplotlib import dates
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import datetime
from datetime import datetime
from astropy.io import fits
from astropy.time import Time
import csv
import scipy.signal
 

# Lists to store data for later
obs_time = []
moon_angular_diameter = []
sun_angular_diameter = []
separation = []
eclipse_data = {}

# Read Moon data
with open("EclipseModels/horizons_results_moon_trimmed.txt") as file:
    for line in file:
        line_contents = line.rstrip().split()
        time = line_contents[0] + ' ' + line_contents[1]
        obs_time.append(datetime.fromisoformat(time))
        moon_angular_diameter.append(float(line_contents[2]) / 3600)
        separation.append(float(line_contents[3]))

# Read Sun data
with open("EclipseModels/horizons_results_sun.txt") as file:
    for line in file:
        line_contents = line.rstrip().split()
        sun_angular_diameter.append(float(line_contents[2]) / 3600)

# Obscuration function
def obscuration(r_sun, r_moon, sep):
    Y = (r_sun**2 - r_moon**2 + sep**2) / (2 * sep)
    if abs(Y) < r_sun:
        alpha_1 = 2 * math.acos(Y / r_sun)
        alpha_2 = 2 * math.acos((sep - Y) / r_moon)
        A1 = 0.5 * r_sun**2 * (alpha_1 - math.sin(alpha_1))
        A2 = 0.5 * r_moon**2 * (alpha_2 - math.sin(alpha_2))
        return (A1 + A2) / (math.pi * r_sun**2)
    elif r_moon > r_sun:
        return 1
    else:
        return r_moon**2 / r_sun**2

# Scaling factors for theoretical radii
scaling_factors = [0.8, 1.0, 1.2, 1.27, 1.5]

# Assume different Solar Radii
for factor in scaling_factors:
    eclipse_percentage = []
    for i in range(len(obs_time)):
        r_sun = (factor * sun_angular_diameter[i]) / 2
        r_moon = moon_angular_diameter[i] / 2
        sep = separation[i]
        
        if sep <= (r_sun + r_moon):
            eclipse_percentage.append(1 - obscuration(r_sun, r_moon, sep))
        else:
            eclipse_percentage.append(1.0)
    
    eclipse_data[factor] = eclipse_percentage

# Plot results
plt.figure(figsize=(10, 5))
for factor in reversed(scaling_factors):  # Reverse order of legend for easier viewing
    plt.plot(obs_time, eclipse_data[factor], label=f"R/Rsun = {factor}")

plt.xlabel("Time")
plt.ylabel("Relative Brightness")
plt.title("Percent Obscuration vs. Time for Theoretical Solar Radii")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.savefig("solar_radius_variation.png")
plt.show()





# The above is just a theoretical model. Below, I will add the Radio Data into a separate graph.


# Load and process radio data
hdu1 = fits.open("data/20240408-171452_TPI-PROJ01-SUN_02#_01#.fits")
data = hdu1[1].data
date = data['jd']
r_pol = data['RIGHT_POL']

# Smooth and normalize radio data
def normalization(lightcurve):
    high = max(lightcurve)
    return lightcurve / high * 100

r_pol_smooth = scipy.signal.savgol_filter(r_pol, 51, 0)
r_pol_normalized = normalization(r_pol_smooth)

# Plot radio data
plt.figure(figsize=(10, 5))
plt.plot(date, r_pol_normalized, label="Smoothed & Normalized Radio Data", color='green')
plt.xlabel("Julian Date")
plt.ylabel("Normalized Signal Strength (%)")
plt.title("Radio Telescope Data During Eclipse")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.savefig("radio_data_plot.png")
plt.show()




# Below is the Linear Adjustment Data


# Data from the fits file
hdu1 = fits.open("data/20240408-171452_TPI-PROJ01-SUN_02#_01#.fits")
data = hdu1[1].data
t = Time(data['jd'], format='jd')
date = data['jd']
t = t.plot_date
r_pol = data['RIGHT_POL']
#len date 9935
# code used to find the indexes of the 1-4 contact
list = [1,2,3,4,5,6,7,8,9,10]

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

#Finds pre1st contact index
for i in range(len(date)):
    if (pre1st - date[i]) < epsilon:
        index_pre = i
        print("found pre1st index", index_pre)
        break

#Finds 1st contact index
for i in range(len(date)):
    if (contact1st - date[i]) < epsilon:
        index_1st = i
        print("found 1st index", index_1st)
        break

#Finds 2nd contact index
for i in range(len(date)):
    if (contact2nd - date[i]) < epsilon:
        index_2nd = i
        print("found 2nd index", index_2nd)
        break

#Finds 3rd contact index
for i in range(len(date)):
    if (contact3rd - date[i]) < epsilon:
        index_3rd = i
        print("found 3rd index", index_3rd)
        break

#Finds 4th contact index
for i in range(len(date)):
    if (contact4th - date[i]) < epsilon:
        index_4th = i
        print("found 4th index", index_4th)
        break

#Finds final data index
for i in range(len(date)):
    if (final - date[i]) < epsilon:
        index_final = i
        print("found final index", index_final)
        break

#Code to calculate line of adjustment
#calculates average magnitude of the amount of time before 1st contact that is available post 4th contact
sum = 0
dif = index_1st - index_pre
for i in range(index_pre, index_1st):
    sum = sum + r_pol[i]
pre_average = sum/dif
print("Average magnitude before 1st contact", pre_average)

#calculates average magnitude after 4th contact
sum = 0
dif = index_final - index_4th
for i in range(index_4th, index_final):
    sum = sum + r_pol[i]
post_average = sum/dif
print("Average magnitude after 4th contact", post_average)

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

#Graphs Data
plt.plot(date, r_pol, label = "Raw Data")#not adjusted Graph
plt.plot(date, r_pol + adjustment_function, label = "Skew Adjusted Data")#adjusted Graph
plt.plot(date, adjustment_function, label = "Linear Adjustment Function")#Linear adjustment
plt.axvline(x = date[index_1st], color = 'r', linestyle = '-') #1st contact
plt.axvline(x = date[index_2nd], color = 'r', linestyle = '-') #2nd contact
plt.axvline(x = date[index_3rd], color = 'r', linestyle = '-') #3rd contact
plt.axvline(x = date[index_4th], color = 'r', linestyle = '-') #4th contact
plt.xlabel("Julian Date")
plt.ylabel("Relative Brightness")

plt.legend()
plt.savefig("linear_adjustment.png")
plt.show()













# All this below is what was originally in this file.
''' 
obs_time = []
moon_angular_diameter = []
sun_angular_diameter = []
separation = []
eclipse_percentage = []
eclipse_percentage_big_sun = []

with open('EclipseModels/horizons_results_moon_trimmed.txt') as file:
    for line in file:
        line_contents = line.rstrip().split()
        time = line_contents[0] + ' ' + line_contents[1]
        obs_time.append(datetime.fromisoformat(time))
        moon_angular_diameter.append(float(line_contents[2])/3600)
        separation.append(float(line_contents[3]))

with open('EclipseModels/horizons_results_sun.txt') as file:
    for line in file:
        line_contents = line.rstrip().split()
        sun_angular_diameter.append(float(line_contents[2])/3600)

# From http://www.jgiesen.de/eclipse/        
def obscuration(r_sun, r_moon, sep):
    Y = (r_sun**2 - r_moon**2 + sep**2)/(2 * sep)
    if abs(Y) < r_sun:
        alpha_1 = 2 * math.acos(Y / r_sun)
        alpha_2 = 2 * math.acos((sep - Y) / r_moon)
        A1 = 0.5 * r_sun**2 * (alpha_1 - math.sin(alpha_1))
        print("A1 = ", A1)
        A2 = 0.5 * r_moon**2 * (alpha_2 - math.sin(alpha_2))
        print("A1 = ", A2)        
        return (A1 + A2) / (math.pi * r_sun**2)
    elif r_moon > r_sun:
        return 1
    else:
        return r_moon**2 / r_sun**2


for i in range(len(obs_time)):
#    print("sun = ", sun_angular_diameter[i]/2)
#    print("moon = ", moon_angular_diameter[i]/2)
#    print("sep = ", separation[i])
    if separation[i] <= (sun_angular_diameter[i]/2 + moon_angular_diameter[i]/2):
        print("Eclipsing!", obs_time[i])
        eclipse_percentage.append(1 - obscuration(sun_angular_diameter[i]/2, moon_angular_diameter[i]/2, separation[i]))
    else:
        eclipse_percentage.append(1.0)

for i in range(len(obs_time)):
#    print("sun = ", sun_angular_diameter[i]/2)
#    print("moon = ", moon_angular_diameter[i]/2)
#    print("sep = ", separation[i])
    sun_angular_diameter[i] = 1.2 * sun_angular_diameter[i]
    if separation[i] <= (sun_angular_diameter[i]/2 + moon_angular_diameter[i]/2):
        print("Eclipsing!", obs_time[i])
        eclipse_percentage_big_sun.append(1 - obscuration(sun_angular_diameter[i]/2, moon_angular_diameter[i]/2, separation[i]))
    else:
        eclipse_percentage_big_sun.append(1.0)

plt.plot(obs_time, eclipse_percentage)
plt.plot(obs_time, eclipse_percentage_big_sun)
plt.savefig("simulation.png")
'''










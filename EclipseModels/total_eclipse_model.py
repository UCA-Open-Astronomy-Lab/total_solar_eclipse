import math
import csv

import matplotlib.pyplot as plt

from datetime import datetime

obs_time = []
moon_angular_diameter = []
sun_angular_diameter = []
separation = []
eclipse_percentage = []
eclipse_percentage_big_sun = []

with open('horizons_results_moon_trimmed.txt') as file:
    for line in file:
        line_contents = line.rstrip().split()
        time = line_contents[0] + ' ' + line_contents[1]
        obs_time.append(datetime.fromisoformat(time))
        moon_angular_diameter.append(float(line_contents[2])/3600)
        separation.append(float(line_contents[3]))

with open('horizons_results_sun.txt') as file:
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
     #   print("A1 = ", A1)
        A2 = 0.5 * r_moon**2 * (alpha_2 - math.sin(alpha_2))
     #   print("A1 = ", A2)        
        return (A1 + A2) / (math.pi * r_sun**2)
    elif r_moon > r_sun:
        return 1
    else:
        return r_moon**2 / r_sun**2


# Rough code to generate a bunch of theoretical curves.

sun_diameter_factors = [1, 1.05, 1.10, 1.15, 1.20, 1.25, 1.27, 1.3, 1.35, 1.4, 1.45]
new_sun_angular_diameter = []

for sun_diameter_factor in sun_diameter_factors:

    print(sun_diameter_factor)

    with open("tse_radius_" + str(sun_diameter_factor) + ".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for i in range(len(obs_time)):

            if separation[i] <= (sun_diameter_factor * sun_angular_diameter[i]/2 + moon_angular_diameter[i]/2):
                eclipse_percentage_big_sun = 1 - obscuration(sun_diameter_factor * sun_angular_diameter[i]/2, moon_angular_diameter[i]/2, separation[i])
                writer.writerow([obs_time[i], eclipse_percentage_big_sun])
            else:
                eclipse_percentage_big_sun = 1.0
                writer.writerow([obs_time[i], eclipse_percentage_big_sun])
                    

#plt.plot(obs_time, eclipse_percentage)
#plt.plot(obs_time, eclipse_percentage_big_sun)
#plt.savefig("simulation.png")











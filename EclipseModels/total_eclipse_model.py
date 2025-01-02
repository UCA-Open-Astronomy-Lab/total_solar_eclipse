import math

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











from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.time import Time
from matplotlib import dates
import numpy as np
import csv

"""Data from the fits file"""
hdu1 = fits.open("data/20240408-171452_TPI-PROJ01-SUN_02#_01#.fits")
data = hdu1[1].data
t = Time(data['jd'], format='jd')
date = data['jd']
t = t.plot_date
r_pol = data['RIGHT_POL']
#len date 9935

"""code used to find the indexes of the 1-4 contact"""
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
count = [329130.0,328012.0,327956.0,328738.0,327722.0,327988.0,327794.0,327651.0,328184.0,327969.0,327945.0,328594.0,328089.0,327479.0,327989.0,327575.0,328260.0,329487.0,328620.0,91537.0,91537.0,91537.0,91537.0,91537.0,91537.0,91537.0,91537.0,327270.0,326814.0,327340.0,326928.0,326945.0,326830.0,327112.0,327619.0,327496.0,318203.0,326485.0,327402.0,329214.0,326571.0,326967.0,325852.0,324336.0,323377.0,320428.0,318938.0,316811.0,315969.0,311274.0,307260.0,310834.0,306247.0,300801.0,297502.0,294383.0,290994.0,287841.0,283870.0,280749.0,277259.0,273539.0,274088.0,265358.0,263629.0,261436.0,253682.0,248831.0,245381.0,241158.0,235814.0,232003.0,227794.0,223203.0,218652.0,214039.0,209341.0,205257.0,199934.0,195439.0,190562.0,185974.0,180575.0,176221.0,171213.0,166185.0,161274.0,156169.0,151150.0,145919.0,140840.0,135823.0,130675.0,125580.0,120299.0,115193.0,109944.0,104623.0,99405.0,93913.0,88778.0,83469.0,78320.0,72890.0,67480.0,62288.0,56868.0,51445.0,46427.0,41357.0,35850.0,30511.0,25360.0,20296.0,15995.0,11838.0,7599.0,4084.0,385693.0,387145.0,251652.0,429056.0,4463.0,8403.0,13721.0,19164.0,20743.0,26009.0,31279.0,36628.0,41979.0,47293.0,52685.0,58112.0,63360.0,68900.0,73995.0,79277.0,84731.0,90067.0,95423.0,100696.0,106106.0,111210.0,116455.0,121397.0,126990.0,132078.0,137315.0,142395.0,147629.0,152635.0,157710.0,162708.0,167722.0,172683.0,177700.0,182575.0,187606.0,192271.0,197135.0,201872.0,206543.0,210915.0,215777.0,220109.0,224970.0,229354.0,234150.0,238851.0,243336.0,247629.0,251705.0,256019.0,259470.0,262357.0,267222.0,270988.0,270647.0,281303.0,283114.0,285961.0,289808.0,292977.0,296250.0,306106.0,303186.0,305689.0,308153.0,310649.0,313936.0,311511.0,313705.0,320668.0,322304.0,322544.0,327178.0,326704.0
]
time = [2460409.2036806,2460409.2043750403,2460409.20506948,2460409.20576392,2460409.20645836,2460409.2071528,2460409.20784724,2460409.20854168,2460409.20923612,2460409.20993056,2460409.210625,2460409.21131944,2460409.2120138803,2460409.21270832,2460409.21340276,2460409.2140972,2460409.21479164,2460409.21548608,2460409.21618052,2460409.21687496,2460409.2175694,2460409.21826384,2460409.21895828,2460409.2196527203,2460409.22034716,2460409.2210416,2460409.22173604,2460409.22243048,2460409.22312492,2460409.22381936,2460409.2245138,2460409.22520824,2460409.22590268,2460409.22659712,2460409.2272915603,2460409.227986,2460409.22868044,2460409.22937488,2460409.23006932,2460409.23076376,2460409.2314582,2460409.23215264,2460409.23284708,2460409.23354152,2460409.23423596,2460409.2349304003,2460409.23562484,2460409.23631928,2460409.23701372,2460409.23770816,2460409.2384026,2460409.23909704,2460409.23979148,2460409.24048592,2460409.24118036,2460409.2418748,2460409.24256924,2460409.24326368,2460409.2439581202,2460409.24465256,2460409.245347,2460409.24604144,2460409.24673588,2460409.24743032,2460409.24812476,2460409.2488192,2460409.24951364,2460409.25020808,2460409.25090252,2460409.2515969602,2460409.2522914,2460409.25298584,2460409.25368028,2460409.25437472,2460409.25506916,2460409.2557636,2460409.25645804,2460409.25715248,2460409.25784692,2460409.25854136,2460409.2592358002,2460409.25993024,2460409.26062468,2460409.26131912,2460409.26201356,2460409.262708,2460409.26340244,2460409.26409688,2460409.26479132,2460409.26548576,2460409.2661802,2460409.2668746402,2460409.26756908,2460409.26826352,2460409.26895796,2460409.2696524,2460409.27034684,2460409.27104128,2460409.27173572,2460409.27243016,2460409.2731246,2460409.27381904,2460409.2745134803,2460409.27520792,2460409.27590236,2460409.2765968,2460409.27729124,2460409.27798568,2460409.27868012,2460409.27937456,2460409.280069,2460409.28076344,2460409.28145788,2460409.2821523203,2460409.28284676,2460409.2835412,2460409.28423564,2460409.28493008,2460409.28562452,2460409.28631896,2460409.2870134,2460409.28770784,2460409.28840228,2460409.28909672,2460409.2897911603,2460409.2904856,2460409.29118004,2460409.29187448,2460409.29256892,2460409.29326336,2460409.2939578,2460409.29465224,2460409.29534668,2460409.29604112,2460409.29673556,2460409.2974300003,2460409.29812444,2460409.29881888,2460409.29951332,2460409.30020776,2460409.3009022,2460409.30159664,2460409.30229108,2460409.30298552,2460409.30367996,2460409.3043744,2460409.30506884,2460409.30576328,2460409.30645772,2460409.30715216,2460409.3078466,2460409.30854104,2460409.30923548,2460409.30992992,2460409.31062436,2460409.3113188,2460409.31201324,2460409.31270768,2460409.31340212,2460409.3140965602,2460409.314791,2460409.31548544,2460409.31617988,2460409.31687432,2460409.31756876,2460409.3182632,2460409.31895764,2460409.31965208,2460409.32034652,2460409.32104096,2460409.3217354002,2460409.32242984,2460409.32312428,2460409.32381872,2460409.32451316,2460409.3252076,2460409.32590204,2460409.32659648,2460409.32729092,2460409.32798536,2460409.3286798,2460409.3293742402,2460409.33006868,2460409.33076312,2460409.33145756,2460409.332152,2460409.33284644,2460409.33354088,2460409.33423532,2460409.33492976,2460409.3356242,2460409.33631864,2460409.3370130803,2460409.33770752,2460409.33840196,2460409.3390964,2460409.33979084,2460409.34048528
]

sum = 0
for i in range(10):
    sum += count[i]
topaverage = sum/10

percentcount = np.array(count)
percentcount = (percentcount*100)/topaverage
percentcount = percentcount.tolist()

print("Radio t0:", date[0])
print("Visual t0:", time[0])


plt.plot(time, percentcount, label = "Adjusted Visual Data")#Linear adjustment

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
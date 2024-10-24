from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.time import Time
from matplotlib import dates

hdu1 = fits.open("./data/20240408-171452_TPI-PROJ01-SUN_02#_01#.fits")

header = hdu1[1].header

data = hdu1[1].data

t = Time(data['jd'], format='jd')

t = t.plot_date

r_pol = data['RIGHT_POL']

fig, ax = plt.subplots()

ax.plot_date(t, r_pol, '-')

ax.set(xlabel='UTC Time', ylabel='ADU (counts)',
       title="2024-04-08 Total Solar Eclipse, Conway, AR 1429.25 MHz")

ax.vlines([Time('2024-04-08T17:33:50.6', format='isot', scale='utc').plot_date], 0, 1, transform=ax.get_xaxis_transform(), colors='r')
ax.vlines([Time('2024-04-08T18:51:04.8', format='isot', scale='utc').plot_date], 0, 1, transform=ax.get_xaxis_transform(), colors='r')
ax.vlines([Time('2024-04-08T18:54:58.0', format='isot', scale='utc').plot_date], 0, 1, transform=ax.get_xaxis_transform(), colors='r')
ax.vlines([Time('2024-04-08T20:11:36.9', format='isot', scale='utc').plot_date], 0, 1, transform=ax.get_xaxis_transform(), colors='r')

ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M:%S"))

ax.grid()

fig.savefig("r_pol.png")
plt.show()



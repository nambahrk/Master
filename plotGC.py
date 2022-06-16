from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read(code):
    #right ascension
    df   = pd.read_csv(code)
    ra1  = df['Ch1'].values

    #declination
    df   = pd.read_csv(code)
    dec1 = df['Ch2'].values

    return ra1,dec1


def Galactic(ra,dec):
    c = SkyCoord(ra=ra, dec=dec, unit='deg')
    c = c.galactic
    RA = np.array(c.l)
    DEC = np.array(c.b)

    x = np.remainder(RA+360,360) # shift RA values
    ind     = x>180
    x[ind] -= 360
    RA      = -x

    tick_labels = np.array([150, 120, 90, 60, 30, 0, -30, -60, -90, -120, -150])
    fig = plt.figure() #make figure object
    ax = fig.add_subplot(111, projection='aitoff') #make axes object
    ax.scatter(np.radians(55),np.radians(19.4), s=100, alpha=0.3 , color="red")
    ax.scatter(np.radians(RA),np.radians(DEC), s=2.5)  # convert degrees to radians
    ax.set_xticklabels(tick_labels)     # we add the scale on the x axis
    ax.set_title("Direction of Arrival (GC)\n @Auger")
    ax.set_xlabel("galactic longitude")
    ax.set_ylabel("galactic latitude")
    ax.grid(True)
    plt.savefig("galactic.jpg")
    plt.show()

ra1,dec1 = read('Auger.csv')
Galactic(ra1, dec1)

from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def read(code):
    #right ascension
    df   = pd.read_csv(code)
    ra1  = df['Ch1'].values

    #declination
    df   = pd.read_csv(code)
    dec1 = df['Ch2'].values

    return ra1,dec1

def plot2d(ra,dec):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    H = ax.hist2d(ra1, dec1, bins=15, cmap=cm.jet)
    ax.set_title('RA-DEC(2D)')
    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')
    fig.colorbar(H[3],ax=ax)
    plt.savefig("plot2d.jpg")
    plt.show()


ra1,dec1 = read('Auger.csv')
plot2d(ra1,dec1)

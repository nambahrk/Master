from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#execute function
def EC(code='Auger.csv',  starRA=201.3, starDEC= -43):
    ra1,dec1 = read(code)
    Equatorial(ra1, dec1, starRA, starDEC)

#code reading
def read(code):
    df   = pd.read_csv(code)
    ra1  = df['Ch1'].values #right ascension
    df   = pd.read_csv(code)
    dec1 = df['Ch2'].values #declination
    return ra1,dec1

#plot Equatorial Coordinates
def Equatorial(ra1, dec1,  starRA=201.3, starDEC= -43):
    ra1  = -ra1
    ra1 -= 180
    c = SkyCoord(ra=ra1, dec=dec1, unit='deg')
    ra_rad  = c.ra.wrap_at(180 * u.deg).radian
    dec_rad = c.dec.radian

    #CentaurusA
    starRA = -starRA
    starRA -= 180
    cc = SkyCoord(starRA, starDEC,unit='deg')
    ra_rad2  = cc.ra.wrap_at(180 * u.deg).radian
    dec_rad2 = cc.dec.radian

    fig = plt.figure() #make figure object
    ax = fig.add_subplot(111, projection='aitoff') #make axes object
    ax.set_title("Direction of Arrival(EC) \n @Auger")
    tick_labels = np.array([330, 300, 270, 240, 210, 180, 150, 120, 90, 60, 30])
    ax.set_xticklabels(tick_labels)
    ax.grid(True)
    ax.plot(ra_rad, dec_rad, 'o', markersize=2,alpha=0.7)
    ax.plot(ra_rad2, dec_rad2, 'o', markersize=10, alpha=0.3, color="red")
    plt.savefig("plotEC.jpg")
    plt.show()

EC()

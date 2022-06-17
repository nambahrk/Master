from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#execute function
def overing2D(code='Auger.csv',angle=28):
    ra,dec = read(code)
    ra,dec = oversample(ra, dec, angle)
    plot(ra, dec, angle)

#code reading
def read(code):
    df  = pd.read_csv(code)
    ra = df['Ch1'].values #right ascension
    df  = pd.read_csv(code)
    dec = df['Ch2'].values #declination
    return ra, dec

#oversample
def oversample(ra, dec, angle=28):
    for i in range(1, len(ra)):
        keido = math.radians(ra[i])
        ido   = math.radians(dec[i])
        a1 = math.cos(ido)*math.sin(keido)
        a2 = math.cos(ido)*math.cos(keido)
        a3 = math.sin(ido)

        for k in range(0,360):
            for j in range(-90,90):
                b1 = math.cos(math.radians(j))*math.sin(math.radians(k))
                b2 = math.cos(math.radians(j))*math.cos(math.radians(k))
                b3 = math.sin(math.radians(j))

                if np.abs((a1*b1+a2*b2+a3*b3)/(np.sqrt(a1**2+a2**2+a3**2)*np.sqrt(b1**2+b2**2+b3**2))) <=1 :
                    angling = math.degrees(math.acos((a1*b1+a2*b2+a3*b3)/(np.sqrt(a1**2+a2**2+a3**2)*np.sqrt(b1**2+b2**2+b3**2))))

                    if angling < angle:
                        ra  = np.append(ra, k)
                        dec = np.append(dec,j)

                    else:
                        pass
                else:
                    pass
    return ra,dec

#plot
def plot(ra,dec,angle):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    H = ax.hist2d(ra,dec, bins=[360,180], range=[[0,360],[-90,90]] ,cmap=cm.jet)
    ax.set_title('RA-DEC(2D,oversampling' + angle + 'degrees)')
    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')
    fig.colorbar(H[3],ax=ax)
    plt.savefig("over2D.jpg")
    plt.show()

overing2D()

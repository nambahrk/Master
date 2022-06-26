from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#execute function
def overingEC(code='Auger.csv',angle=28):
    ra,dec = read(code)
    ra,dec = oversample(ra, dec, angle)
    plot(ra, dec,angle)

#code reading
def read(code):
    df  = pd.read_csv(code)
    ra = df['Ch1'].values #right ascension
    df  = pd.read_csv(code)
    dec = df['Ch2'].values #declination
    return ra, dec

#oversample
def oversample(ra,dec,angle):
    for i in range(1,len(ra)):
        keido = math.radians(ra[i])
        ido = math.radians(dec[i])
        a1 = math.cos(ido)*math.sin(keido)
        a2 = math.cos(ido)*math.cos(keido)
        a3 = math.sin(ido)

        for k in range(0,360):
            for j in range(-90, 90):
                b1 = math.cos(math.radians(j))*math.sin(math.radians(k))
                b2 = math.cos(math.radians(j))*math.cos(math.radians(k))
                b3 = math.sin(math.radians(j))

                if np.abs((a1*b1+a2*b2+a3*b3)/(np.sqrt(a1**2+a2**2+a3**2)*np.sqrt(b1**2+b2**2+b3**2))) <=1 :
                    angling = math.degrees(math.acos((a1*b1+a2*b2+a3*b3)/(np.sqrt(a1**2+a2**2+a3**2)*np.sqrt(b1**2+b2**2+b3**2))))

                    if angling < angle:
                        ra = np.append(ra, float(k))
                        dec = np.append(dec, float(j))

                    else:
                        pass
                else:
                    pass
    return ra,dec

def plot(RA, Dec,angle):
    RA  = -RA
    RA += 180

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection='aitoff')
    z, _, _ = np.histogram2d(RA, Dec, bins=[360,180], range=[[-180,180],[-90, 90]])
    ra = np.linspace(-np.pi, np.pi, 360)
    dec = np.linspace(-np.pi/2 , np.pi/2, 180)
    Ra, Dec = np.meshgrid(ra, dec)
    im = ax.pcolormesh(Ra, Dec, z.T, cmap=cm.jet)

    tick_labels = np.array([330, 300, 270, 240, 210, 180, 150, 120, 90, 60, 30])
    ax.set_xticklabels(tick_labels)
    ax.set_title('RA-DEC(EC,oversampling' + str(angle) + 'degrees)')
    ax.set_xlabel("Right Ascension")
    ax.set_ylabel("Declination")
    ax.grid(True)
    fig.colorbar(im,ax=ax)
    plt.savefig("overEC.jpg")
    plt.show()

overingEC()

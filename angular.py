from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


#execute function
def angularhist(code='Auger.csv', bins=180):
    rightascention, declination = read(code)
    plot(accumulation(rightascention, declination),bins)

#code reading
def read(code):
    #right ascension
    df = pd.read_csv(code)
    rightascention = df['Ch1'].values

    #declination
    df = pd.read_csv(code)
    declination = df['Ch2'].values

    return rightascention, declination

#accumulation analysis
def accumulation(ra,dec):
    #centaurus A direction vector
    a1 = math.cos(math.radians(-43))*math.sin(math.radians(201))
    a2 = math.cos(math.radians(-43))*math.cos(math.radians(201))
    a3 = math.sin(math.radians(-43))

    c = SkyCoord(ra=ra, dec=dec, unit='deg')
    alpha   = c.ra.radian
    delta   = c.dec.radian
    number  = len(ra)
    angular = np.empty(0)

    for i in range(number):
        b1 = math.cos(delta[i])*math.sin(alpha[i])
        b2 = math.cos(delta[i])*math.cos(alpha[i])
        b3 = math.sin(delta[i])
        angular = np.append(angular, math.degrees(math.acos((a1*b1+a2*b2+a3*b3)/(np.sqrt(a1**2+a2**2+a3**2)*np.sqrt(b1**2+b2**2+b3**2)))))

    return angular

#plot
def plot(angular, bins=180):
    fig = plt.figure() #make figure object
    ax = fig.add_subplot(111) #make axes object
    ax.hist(angular, bins, (0, 180), cumulative=True)
    ax.set_title("Angular Distance from Cen A")
    ax.set_xlabel("Angular")
    ax.set_ylabel("Count")
    plt.savefig("Angular.jpg")
    plt.show()

angularhist()    

from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#execute function
def data(code='dipole.csv'):
    zenith,azimuth,year,month,day,hour,min,sec = read(code)
    locallst=lst(year,month,day,hour,min,sec)
    ra,dec=change(zenith, azimuth,locallst)
    plot(zenith, azimuth, ra, dec)

#return function
def datas(code='dipole.csv'):
    zenith,azimuth,year,month,day,hour,min,sec = read(code)
    locallst=lst(year,month,day,hour,min,sec)
    ra,dec=change(zenith, azimuth,locallst)
    return ra,dec


#code reading
def read(code):
    year  = np.empty(0)
    month = np.empty(0)
    day   = np.empty(0)
    hour  = np.empty(0)
    min   = np.empty(0)
    sec   = np.empty(0)
    df    = pd.read_csv(code)
    when    = df['Ch1'].values
    time    = df['Ch2'].values
    zenith  = df['Ch6'].values
    azimuth = df['Ch7'].values

    for i in range(len(when)):
        wh =(when[i])%(10**(8))
        y=math.floor(wh/(10**(4)))
        year=np.append(year,y)
        wh =(when[i])%(10**(4))
        m=math.floor(wh/(10**(2)))
        month=np.append(month,m)
        wh =(when[i])%(10**(2))
        d=math.floor(wh/(10**(0)))
        day=np.append(day,d)

    for i in range(len(time)):
        ti =(time[i])%(10**(6))
        h=math.floor(ti/(10**(4)))
        hour=np.append(hour,h)
        ti =(time[i])%(10**(4))
        n=math.floor(ti/(10**(2)))
        min=np.append(min,n)
        ti =(time[i])%(10**(4))
        s=math.floor(ti/(10**(2)))
        sec=np.append(sec,s)

    return zenith,azimuth,year,month,day,hour,min,sec


def lst(year,month,day,hour,min,sec):
    locallst=np.empty(0)
    for i in range(len(year)):
        if month[i]<3:
            month[i]=month[i]+12
            year[i]=year[i]-1

        aa = math.floor(year[i]/100)
        bb = 2-aa+int(aa/4)
        jd = int(365.25*year[i])+int(30.6001*(month[i]+1))+day[i]+bb+1720994.5

        t=(jd-2451545)/36525
        utc = hour[i] + min[i]/24 + sec[i]/1440
        ret = 6.697374558 + 1.0027379093*utc + 2400.051336*t + 0.000025862*t*t

        if ret>24:
            ret = ret-(int(ret/24))*24
        else:
            pass

        local = ret+113/15

        newlocal    = (local-int(local))*100
        newnewlocal = (newlocal-int(newlocal))*100
        locals      = int(local)*15+int(newlocal)*0.25+int(newnewlocal)*15/3600
        locallst    = np.append(locallst,locals)

    return locallst

#change function
def change(zenith, azimuth,locallst):
    ra=np.empty(0)
    dec=np.empty(0)
    phi= 39#ido
    for i in range(len(zenith)):
        z = zenith[i]
        a = azimuth[i]

        decdec = math.degrees(math.asin(math.cos(math.radians(z))*math.sin(math.radians(phi))-math.sin(math.radians(z))*math.cos(math.radians(phi))*math.cos(math.radians(a))))
        rarabefore = math.degrees(math.asin((math.sin(math.radians(z))*math.sin(math.radians(a)))/(math.cos(math.radians(decdec)))))

        if rarabefore<0:
            rarabefore=rarabefore+360
        else:
            pass

        ras= locallst[i]-rarabefore

        ra  = np.append(ra,ras)
        dec = np.append(dec,decdec)

    return ra, dec

#plot
def plot(zenith, azimuth, ra, dec):
    fig = plt.figure() #make figure object

    ax1 = fig.add_subplot(221)
    ax1.hist(zenith, bins=60, range=(0, 60))
    ax1.set_xlabel("zenith angle(degree)")
    ax1.set_ylabel("Entries")

    ax2 = fig.add_subplot(222)
    ax2.hist(azimuth, bins=120, range=(0, 360))
    ax2.set_xlabel("azimuth angle(degree)")
    ax2.set_ylabel("Entries")

    ax3 = fig.add_subplot(223)
    ax3.hist(dec, bins=90, range=(-20,90))
    ax3.set_xlabel("declination(degree)")
    ax3.set_ylabel("Entries")

    ax4 = fig.add_subplot(224)
    ax4.hist(ra, bins=120, range=(0, 360))
    ax4.set_xlabel("right ascention(degree)")
    ax4.set_ylabel("Entries")

    plt.savefig("dipoledata.jpg")
    plt.tight_layout() #prevent overlap
    plt.show()

data()

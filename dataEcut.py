from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#execute function
def data(code='dipole.csv'):
    zenith,azimuth,year,month,day,hour,min,sec,count1,count2,count3 = read(code)
    locallst=lst(year,month,day,hour,min,sec)
    ra,dec=change(zenith, azimuth,locallst)
    plot(zenith, azimuth, ra, dec, count1, count2, count3)

#return function
def datas(code='dipole.csv'):
    zenith,azimuth,year,month,day,hour,min,sec = read(code)
    locallst=lst(year,month,day,hour,min,sec)
    ra,dec=change(zenith, azimuth,locallst)
    return ra,dec

#code reading
def read(code):
    df = pd.read_csv(code)
    when2    = df['Ch1'].values
    time2    = df['Ch2'].values
    zenith2  = df['Ch6'].values
    azimuth2 = df['Ch7'].values
    energy2  = df['Ch10'].values
    count1 = 0
    count2 = 0
    count3 = 0
    energy = np.empty(0)
    zenith = np.empty(0)
    azimuth= np.empty(0)
    when   = np.empty(0)
    time   = np.empty(0)
    year   = np.empty(0)
    month  = np.empty(0)
    day    = np.empty(0)
    hour   = np.empty(0)
    min    = np.empty(0)
    sec    = np.empty(0)

    for j in range(len(energy2)):
        if energy2[j]<5:
            energy  = np.append(energy, energy2[j])
            zenith  = np.append(zenith,zenith2[j])
            azimuth = np.append(azimuth,azimuth2[j])
            when    = np.append(when,when2[j])
            time    = np.append(time,time2[j])
            count1 += 1

    for j in range(len(energy2)):
        if 5<energy2[j]<10:
            energy  = np.append(energy, energy2[j])
            zenith  = np.append(zenith,zenith2[j])
            azimuth = np.append(azimuth,azimuth2[j])
            when    = np.append(when,when2[j])
            time    = np.append(time,time2[j])
            count2 += 1

    for j in range(len(energy2)):
        if 10<energy2[j]:
            energy  = np.append(energy, energy2[j])
            zenith  = np.append(zenith,zenith2[j])
            azimuth = np.append(azimuth,azimuth2[j])
            when    = np.append(when,when2[j])
            time    = np.append(time,time2[j])
            count3 += 1

    for i in range(len(when)):
        wh =(when[i])%(10**(8))
        y=math.floor(wh/(10**(4)))
        wh =(when[i])%(10**(4))
        m=math.floor(wh/(10**(2)))
        wh =(when[i])%(10**(2))
        d=math.floor(wh/(10**(0)))
        year  = np.append(year,y)
        month = np.append(month,m)
        day   = np.append(day,d)

    for i in range(len(time)):
        ti =(time[i])%(10**(6))
        h=math.floor(ti/(10**(4)))
        ti2 =(time[i])%(10**(4))
        n=math.floor(ti2/(10**(2)))
        ti3 =(time[i])%(10**(2))
        s=math.floor(ti3/(10**(0)))
        hour = np.append(hour,h)
        min  = np.append(min,n)
        sec  = np.append(sec,s)

    return zenith,azimuth,year,month,day,hour,min,sec,count1,count2,count3

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
def plot(zenith, azimuth, ra, dec, count1, count2, count3):
    fig = plt.figure() #make figure object

    zenith1=zenith[0:count1]
    zenith2=zenith[count1:count1+count2]
    zenith3=zenith[count1+count2:count1+count2+count3]
    azimuth1=azimuth[0:count1]
    azimuth2=azimuth[count1:count1+count2]
    azimuth3=azimuth[count1+count2:count1+count2+count3]
    ra1=ra[0:count1]
    ra2=ra[count1:count1+count2]
    ra3=ra[count1+count2:count1+count2+count3]
    dec1=dec[0:count1]
    dec2=dec[count1:count1+count2]
    dec3=dec[count1+count2:count1+count2+count3]

    ax1 = fig.add_subplot(221)
    ax1.hist(zenith1, bins=60, density = True, range=(0, 60), alpha = 0.7, label='E<5EeV')
    ax1.hist(zenith2, bins=60, density = True, range=(0, 60), alpha = 0.7, label='5EeV<E<10EeV')
    ax1.hist(zenith3, bins=60, density = True, range=(0, 60), alpha = 0.7, label='10EeV<E')
    ax1.set_xlabel("zenith angle(degree)")
    ax1.set_ylabel("Entries")

    ax2 = fig.add_subplot(222)
    ax2.hist(azimuth1, bins=120, density = True, range=(0, 360), alpha = 0.7, label='E<5EeV')
    ax2.hist(azimuth2, bins=120, density = True, range=(0, 360), alpha = 0.7, label='5EeV<E<10EeV')
    ax2.hist(azimuth3, bins=120, density = True, range=(0, 360), alpha = 0.7, label='10EeV<E')
    ax2.set_xlabel("azimuth angle(degree)")
    ax2.set_ylabel("Entries")

    ax3 = fig.add_subplot(223)
    ax3.hist(dec1, bins=90, density = True, range=(-20, 90), alpha = 0.7, label='E<5EeV')
    ax3.hist(dec2, bins=90, density = True, range=(-20, 90), alpha = 0.7, label='5EeV<E<10EeV')
    ax3.hist(dec3, bins=90, density = True, range=(-20, 90), alpha = 0.7, label='10EeV<E')
    ax3.set_xlabel("declination(degree)")
    ax3.set_ylabel("Entries")

    ax4 = fig.add_subplot(224)
    ax4.hist(ra1, bins=120, density = True, range=(0, 360), alpha = 0.7, label='E<5EeV')
    ax4.hist(ra2, bins=120, density = True, range=(0, 360), alpha = 0.7, label='5EeV<E<10EeV')
    ax4.hist(ra3, bins=120, density = True, range=(0, 360), alpha = 0.7, label='10EeV<E')
    ax4.set_xlabel("right ascention(degree)")
    ax4.set_ylabel("Entries")

    plt.legend(loc='upper right')
    plt.savefig("dipoledata.jpg")
    plt.tight_layout() #prevent overlap
    plt.show()

data()

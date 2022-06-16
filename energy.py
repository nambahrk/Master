import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.modeling import models


def read(code):
    df  = pd.read_csv(code)
    energy = df['Ch3'].values
    return energy

def plot(energy, bins=50):
    fig = plt.figure() #make figure object
    ax  = fig.add_subplot(111) #make axes object
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.hist(energy, bins=50, range=(50, 100))
    ax.set_title("Auger Energy")
    ax.set_xlabel("log Energy(EeV)")
    ax.set_ylabel("log Count")
    plt.savefig("energy.jpg")
    plt.show()


energy = read('Auger.csv')
plot(energy,50)

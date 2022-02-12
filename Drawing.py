
import svgpathtools as svg
from scipy.integrate import trapz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def complex_quad(func, t_vals):
    #compute integral of a complex function over the interval t
    real = np.real(func)
    imag = np.imag(func)
    i = 1j

    real_integral = trapz(real, t_vals)
    imag_integral = i * trapz(imag, t_vals)
    return real_integral + imag_integral


def Fourier(Paths_DF, levels):
    #parameterization of f as a piecewise function given Paths_DF
    def f(t):
        Filter = Paths_DF["time"].values < t
        loc = Paths_DF.iloc[0, 0]
        if True in Filter:
            loc = Paths_DF[Filter].iloc[-1, 0]
        #print(np.polyval(loc.poly(), t))
        return np.polyval(loc.poly(), t)
    superposition = 0

    size = 1000 #number of slices from 0 to 1
    i = 1j
    t_vals = np.linspace(0, 1, size)

    vals = np.array(list(map(f, t_vals)))#map the function f over the interval 0 <= t < 1

    for n in range (-levels, levels + 1):

        exp = np.exp(- 2 * n * np.pi * i * t_vals)
        #exponential component

        c = complex_quad(vals * exp, t_vals)
        #constant component

        superposition += c * exp
        #summation of each level n
    real = np.real(superposition)
    imag = np.imag(superposition)

    #return real, imag as a tuple
    return real, imag



def mag(a, b):
    return np.sqrt(a**2 + b**2)
def arc_length(poly, t1, t2):
    #first, compute derivative of the polynomial
    deriv = np.polyder(poly)

    #split interval of t into 100 subsections to estimate integral
    t_vals = np.linspace(t1, t2, 100)

    #evaluate derivative at each point
    DF = pd.DataFrame({"time": t_vals})
    DF = DF.assign(deriv_real = np.polyval(deriv, t_vals).real)
    DF = DF.assign(deriv_imag = np.polyval(deriv, t_vals).imag)

    #compute magnitude of derivative at each point, then integrate over t
    DF = DF.assign(magnitude = mag(DF["deriv_real"].values, DF["deriv_imag"].values)).drop(columns = ["deriv_real", "deriv_imag"])


    return trapz(DF["magnitude"], DF["time"])

if __name__ == '__main__':

    ###TO CHANGE FILES:
    #add file to the project directory and change the line below this one to match the name of the new file
    #...svg2paths2("<filename>.svg")
    paths, attributes, svg_attributes = svg.svg2paths2("witch-by-loginueveilustra-silhouette.svg")

    paths = paths[0]
    Paths_DF = pd.DataFrame({"Path": paths, "Length": paths.length()})
    total_length = Paths_DF["Length"].values.sum()
    Paths_DF = Paths_DF.assign(percent_length = Paths_DF["Length"] / total_length).drop(columns = "Length")

    #percent length will equal the amount of time that the function should spend on that path
    Paths_DF = Paths_DF.assign(time = Paths_DF["percent_length"].cumsum()).drop(columns = "percent_length")


    Fourier_approx_real, Fourier_approx_imag = Fourier(Paths_DF, 100)

    plt.plot(Fourier_approx_real, Fourier_approx_imag)
    plt.gca().invert_yaxis()
    plt.show()

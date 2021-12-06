import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import trapz
import scipy
from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *

def plot_fourier(x_vals, y_vals, levels):
    L = x_vals[-1]
    superposition = y_vals.mean()
    for i in range(0,levels):
        n = i + 1

        cos_func = np.cos((2 * n * np.pi * x_vals) / L)
        sin_func = np.sin((2 * n * np.pi * x_vals) / L)

        A_func = y_vals * cos_func
        A = (2/L) * trapz(A_func, x_vals)

        B_func = y_vals * sin_func
        B = (2/L) * trapz(B_func, x_vals)

        function = A * cos_func + B * sin_func
        superposition += function
    plt.plot(x_vals, superposition)

if __name__ == '__main__':



    x = np.arange(0, 10, 0.001)
    y = x**4 + 3 * x**2
    plt.plot(x, y)
    plot_fourier(x, y, 10)
    plt.show()




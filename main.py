import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import trapz
import scipy
from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *


image_array = None
def save():
    #return numpy array for image
    global image_array
    image_array = np.array(output_image.getdata())
    master.destroy()

def paint(event):
    x1, y1 = (event.x - 1), (event.y)
    x2, y2 = (event.x + 1), (event.y)
    canvas.create_oval(x1, y1, x2, y2, fill="black",width=2)
    draw.line([x1, y1, x2, y2],fill="black",width=2)

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


def get_poly(x_vals, y_vals, degree):
    coeff_arr = np.polyfit(x_vals, y_vals, degree)
    poly = 0
    for i in range(0, degree + 1):
        poly += coeff_arr[i] * x_vals**(degree - i)
    return poly


if __name__ == '__main__':
    width = 400  # canvas width
    height = 400  # canvas height
    center = height // 2
    white = (255, 255, 255)  # canvas back

    master = Tk()

    # create a tkinter canvas to draw on
    canvas = Canvas(master, width=width, height=height, bg='white')
    canvas.pack()

    # create an empty PIL image and draw object to draw on
    output_image = PIL.Image.new("RGB", (width, height), white)
    draw = ImageDraw.Draw(output_image)
    canvas.pack(expand=YES, fill=BOTH)
    canvas.bind("<B1-Motion>", paint)

    # add a button to save the image
    button = Button(text="save", command=save)
    button.pack()


    master.mainloop()

    arr = np.where(image_array[:, 0] < 255)
    y = np.subtract(height, np.divide(arr, height)[0])
    x = np.mod(arr, width)[0]

    x_order = np.argsort(x)
    x = x[x_order]
    y = y[x_order]

    plt.scatter(x, y)
    #poly = get_poly(x, y, 100)
    #plt.plot(x, poly)
    # x = np.arange(0, 10, 0.001)
    # y = x**4 + 3 * x**2
    # plt.plot(x, y)
    plot_fourier(x, y, 50)
    plt.show()




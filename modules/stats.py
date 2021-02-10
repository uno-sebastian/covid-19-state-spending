import matplotlib as plt
import pandas as pd
from scipy.stats import linregress
import numpy as np

def regression_plot(df, filename, titles, xlabel, ylabel, dotcolor, linecolor, equation_color, eq_locx, eq_locy):
    x_values = df[xlabel]
    y_values = df[ylabel]

    (slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
    regress_values = x_values * slope + intercept

    line_equation = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))

    fig1, ax1 = plt.subplots()
    plt.scatter(x_values,y_values,color=dotcolor)
    plt.plot(x_values,regress_values,color=linecolor)
    plt.title(titles[0])
    plt.xlabel(titles[1])
    plt.ylabel(titles[2])
    ax1.annotate(line_equation, xy=(eq_locx, eq_locy),fontsize=14,color=equation_color)

    plt.savefig(f"../output_data/{filename}.png")
    plt.show()
    return

def bar(xvalues, yvalues):

    plt.pyplot.bar(xvalues,yvalues)
    plt.pyplot.show()
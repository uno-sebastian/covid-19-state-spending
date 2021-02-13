import os
import pandas
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress, pearsonr

money = 'Amount Committed/Disbursed'

start_date = dt.date(2020, 2, 1)
end_date = dt.date(2021, 2, 4)

def where_save(figname):
    return os.path.join('.','output_figures',figname)

def clean_check(dataframe):
    column_name = []
    if dataframe.all().all() == True:
        print(' Great News! your dataset is complete')
    else:
        print("UhOh, at least one of the column contains 'invalid' data (0., NA, NULL)")
        for x, ddf in enumerate(dataframe.all()):
            if ddf == False:
                print('The column '+ dataframe.columns[x] +' has problems')
                column_name.append(dataframe.columns[x])
    return(column_name)


#converting the dates in timestamp - it will serve the purpose later on probably
def adding_timestamp(dataframe):
    try:
        dates = dataframe['Date'].to_list()
    except:
        dates = dataframe['date'].to_list()
    timestamp = [dt.datetime.timestamp(dates[x]) for x, date in enumerate(dates) ]
    dataframe['Timestamp'] = timestamp
    return(dataframe)


def bar_plot(labels, bars, title,figname=None):
    fig, ax = plt.subplots(figsize=(15,8))

    labels = labels.to_list()
    width = 0.4  # the width of the bars
    x = np.arange(len(labels))
    try:
        ax.bar(x,bars, width)
    except:
        column = list(bars.columns)
        for idx, c in enumerate(column):
            a = -width/2*idx
            ax.bar(x+a,bars[c],width,label=column[idx])
            ax.legend(fontsize=(15))


    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average '+ money +' ($)', fontsize = (18))
    ax.set_title(title, fontsize = (25))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize = (17), rotation = 'vertical')
    plt.yticks(fontsize=18)
    plt.tight_layout()
    if figname != None:
        plt.savefig(figname, dpi=300, transparent=True)

    return(plt.show())

# you need datetime to run this set of commands 

def two_y_linear_plot(x1, y1, x2, y2, y2label, y2max, figtitle, figname=None, sd=start_date, ed=end_date, fontsize=18):
    """
    plot a two y linear plot
    
    Parameters
    ----------
        x1 — x1 axis data
        x2 — x2 axis data
        y1 — y1 axis data
        y2 — y2 axis data
        y2label — y axis label
        y2max — y axis max
        title — figure title
        figname — figure file name
        fontsize — figure font size
    """
    fig, ax = plt.subplots(figsize=(10,8))
    ax.plot(x1,y1, ls = 'none', marker = '*', markersize = 10, color = 'black') 
    plt.ylabel('Cumulative '+money+' ($)', fontsize = (fontsize))
    plt.xlabel('Date', fontsize = (fontsize))
    plt.title(figtitle, fontsize = (fontsize*1.4))
    plt.yticks(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.ylim(0,20000000000)
    plt.xlim(sd,ed)
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(x2,y2, '-b')
    ax2.set_ylabel(y2label,color="blue",fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.ylim(0,y2max+5000)
    plt.tight_layout()
    if figname != None:
        plt.savefig(figname, dpi=300, transparent=True)
    plt.show()
    return

def linear_regression_plot(x,y, xlabel, ylabel, title, figname, fontsize=18):
    """
    The Pearson correlation coefficient measures the linear relationship between two datasets.
    Strictly speaking, Pearson’s correlation requires that each dataset be normally distributed. 
    Like other correlation coefficients, this one varies between -1 and +1 with 0 implying no correlation. 
    Correlations of -1 or +1 imply an exact linear relationship.    
    
    Parameters
    ----------
        x — x axis data
        y — y axis data
        xlabel — x axis label
        ylabel — y axis label
        title — figure title
        figname — figure file name
        fontsize — figure font size
    """
    slope, intercept, r_value, p_value, std_err = linregress(x,y)
    #
    correlation = pearsonr(x,y)
    plt.figure(figsize=(10,8))
    plt.plot(x,y, ls = 'None', marker = 'o', color ='green')
    plt.plot(x, slope*x+intercept, '--k')
    plt.xlabel('Cumulative Covid '+xlabel,fontsize=(fontsize))
    plt.ylabel(ylabel,fontsize=(fontsize))
    plt.title(title+ ' - Pearson Coefficient = '+"{:.2f}".format(correlation[0]), fontsize=(fontsize*1.4))
    plt.yticks(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.ylim(0,20000000000)
    plt.tight_layout()
    plt.savefig(figname, dpi=300, transparent=True)
    plt.show()
    return

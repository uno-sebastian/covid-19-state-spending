import os
import pandas
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

import matplotlib.pyplot as plt
import numpy as np
money = 'Amount Committed/Disbursed'
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
    ax.set_ylabel('Average '+money+' ($)', fontsize = (18))
    ax.set_title(title, fontsize = (25))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize = (17), rotation = 'vertical')
    plt.yticks(fontsize=18)
    plt.tight_layout()
    if figname != None:
        plt.savefig(figname, dpi=300, transparent=True)

    return(plt.show())

import datetime as dt    
start_date = dt.date(2020, 2, 1)
end_date = dt.date(2021, 2, 4)
def two_y_linear_plot(x1, y1, x2, y2, y2label, y2max, figtitle, figname = None, sd = start_date, ed = end_date ):
    fig, ax = plt.subplots(figsize=(10,8))
    ax.plot(x1,y1, ls = 'none', marker = '*', markersize = 10, color = 'black') 
    plt.ylabel(money+' ($)', fontsize = (18))
    plt.xlabel('Date', fontsize = (18))
    plt.title(figtitle, fontsize = (25))
    plt.yticks(fontsize=18)
    plt.xticks(fontsize=18)
    plt.ylim(0,900000000)
    plt.xlim(sd,ed)
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(x2,y2, '-b')
    ax2.set_ylabel(y2label,color="blue",fontsize=18)
    plt.yticks(fontsize=18)
    plt.ylim(0,y2max)
    plt.tight_layout()
    if figname != None:
        plt.savefig(figname, dpi=300, transparent=True)
    plt.show()
    return
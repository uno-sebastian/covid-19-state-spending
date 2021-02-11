from modules import covid, crfb
import pandas as pd
import datetime as dt
from scipy.stats import linregress
import matplotlib.pyplot as plt


def get():
    # Grab both dataframes using module defs
    crfb_df = crfb.get_data_single()
    crfb_df.rename(columns={"Recipient State":"state", "Date":"date", "Amount Committed/Disbursed": "money recieved", "Legislation": "legislation"}, inplace=True)
    covid_df = covid.get_data(date_min=dt.datetime(2020, 2, 14), date_max=dt.datetime(2021, 2, 10))

    # Group bys
    us_spend_frame = crfb_df.groupby(['date', 'state'])['money recieved'].sum()
    merge_frame = pd.merge(us_spend_frame, covid_df, on=['date', 'state'])
    merge_frame['timestamp'] = merge_frame[['date']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)
    return merge_frame


def get_start_end(startyear,startmonth,startday,endyear,endmonth,endday):
    # Grab both dataframes using module defs
    crfb_df = crfb.get_data_single()
    crfb_df.rename(columns={"Recipient State":"state", "Date":"date", "Amount Committed/Disbursed": "money recieved", "Legislation": "legislation"}, inplace=True)
    covid_df = covid.get_data(date_min=dt.datetime(startyear, startmonth, startday), date_max=dt.datetime(endyear, endmonth, endday))

    # Group bys
    us_spend_frame = crfb_df.groupby(['date', 'state'])['money recieved'].sum()
    merge_frame = pd.merge(us_spend_frame, covid_df, on=['date', 'state'])
    return merge_frame


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

    #plt.savefig(f"../output_data/{filename}.png")
    plt.show()
    return
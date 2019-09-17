# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:29:54 2018
@author: Yulong Wang
"""

import pickle
import datetime as dttm
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.dates as dt
from datetime import datetime
import matplotlib.pyplot as plt

## 01
def mod_col(df):
    column_name = df.columns.values.tolist()
    if column_name[0] != "STATION":
        df.drop(["STATION0", "VOLT(V)", "STATUS"], axis = 1, inplace = True)
        #df.drop(["STATION0"], axis = 1, inplace = True)
    else:
        df.drop(["STATION", "VOLT(V)", "STATUS"], axis = 1, inplace = True)
        #df.drop(["STATION"], axis = 1, inplace = True)
    df_mc = [int(i[0:4]) for i in df["DATE & TIME"]]
    df["YEAR"] = df_mc
    #column_name = df.columns.values.tolist()
    return df

## 03-01
def wash_noise(df, col_name, num):
    df_te = df[(df[col_name] - df[col_name].mean()).abs() <= num * df[col_name].std()]
    print("There are " + str(len(df) - len(df_te)) + " lines of " + col_name + " data are dropped.")
    return df_te

## 05
def make_array(df):
    #name = [i for i in df.columns.values.tolist()]
    df_dt = np.array([datetime.strptime(str(i), "%Y/%m/%d %H:%M:%S") for i in df["DATE & TIME"]])
    df_dt = np.array([dt.date2num(i) for i in df_dt])
    #df_sn = np.array([i for i in df["SEQ_NO"]])
    df_dp = np.array([i for i in df["DEPTH(m.DL)"]])
    df_te = np.array([i for i in df["TEMP(deg)"]])
    df_ch = np.array([i for i in df["Chl-a(ug/l)"]])
    df_sa = np.array([i for i in df["SAL(psu)"]])
    df_ss = np.array([i for i in df["SS(mg/l)"]])
    #df_dd = np.array([i for i in df["DO(%)"]])
    df_do = np.array([i for i in df["DO(mg/l)"]])
    #df_bo = np.array([i for i in df["BOTTOM(m)"]])
    return df_dt.T, df_dp.T, df_te.T, df_ch.T, df_sa.T, df_ss.T, df_do.T

## 02
def choose_year(df, year_b, year_e):
    df = df[df["YEAR"] >= year_b]
    df = df[df["YEAR"] <= year_e]
    return df

## 04
def uniform_time(df, year_b, year_e):
    date1 = dttm.datetime(year_b, 1, 1, 0, 0, 0, 0)
    date2 = dttm.datetime(year_e + 1, 1, 1, 0, 0, 0, 0)
    delta = dttm.timedelta(hours = 1)
    dates = dt.drange(date1, date2, delta)
    dateframe = pd.DataFrame({"DATE & TIME":[], "uniform_time":[]})
    dateframe["uniform_time"] = [i for i in dates]
    dateframe["DATE & TIME"] = [i.strftime("%Y/%m/%d %H:%M:%S") for i in dt.num2date(dates)]
    df_ut = dateframe.merge(df, on = ["DATE & TIME"], how = "outer")
    return df_ut

## 03
def prepare_data(df):
    df = wash_noise(df, "TEMP(deg)", 3)
    df = wash_noise(df, "Chl-a(ug/l)", 3)
    df = wash_noise(df, "SAL(psu)", 3)
    df = wash_noise(df, "SS(mg/l)", 3)
    df = wash_noise(df, "DO(mg/l)", 3)
    return df

def plot_values(df_dt, df_dp, df_te, df_ch, df_sa, df_ss, df_do, year_b, year_e):
    g_ratio = (1. + np.sqrt(5.)) / 2.
    f_width = 7.48
    figsize = (f_width, f_width / g_ratio * 5 / 3)
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows = 5, sharex = 'col', figsize = figsize)
    fig.autofmt_xdate()
    
    #ax1.tricontour(df_dt, df_dp, df_te, 20, linewidths = 0.0, colors = 'k')
    cntr = ax1.tricontourf(df_dt, df_dp, df_te, 200, cmap = "jet")
    cb = plt.colorbar(cntr, ax=ax1)
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    cb.set_label('Temp. [degC]')
    #formatter = dt.DateFormatter('%Y-%m-%d')
    #ax1.xaxis.set_major_formatter(formatter)
    ax1.set_ylim((df_dp.min(), 0))
    ax1.set_ylabel("z [m]")
    
    #ax2.tricontour(df_dt, df_dp, df_sa, 20, linewidths = 0.0, colors = 'k')
    cntr = ax2.tricontourf(df_dt, df_dp, df_sa, 200, cmap = "jet")
    cb = plt.colorbar(cntr, ax=ax2)
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    cb.set_label('Salinity [psu]')
    #formatter = dt.DateFormatter('%Y-%m-%d')
    #ax2.xaxis.set_major_formatter(formatter)
    ax2.set_ylim((df_dp.min(), 0))
    ax2.set_ylabel("z [m]")
    
    #ax3.tricontour(df_dt, df_dp, df_ch, 20, linewidths = 0.0, colors = 'k')
    cntr = ax3.tricontourf(df_dt, df_dp, df_ch, 200, cmap = "jet")
    cb = plt.colorbar(cntr, ax=ax3)
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    cb.set_label('Chl-a [ug/l]')
    #formatter = dt.DateFormatter('%Y-%m-%d')
    #ax3.xaxis.set_major_formatter(formatter)
    ax3.set_ylim((df_dp.min(), 0))
    ax3.set_ylabel("z [m]")
    
    #ax5.tricontour(df_dt, df_dp, df_ss, 20, linewidths = 0.0, colors = 'k')
    cntr = ax5.tricontourf(df_dt, df_dp, df_ss, 200, cmap = "jet")
    cb = plt.colorbar(cntr, ax=ax5)
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    cb.set_label('SS [mg/l]')
    formatter = dt.DateFormatter('%Y-%m-%d')
    ax5.xaxis.set_major_formatter(formatter)
    ax5.set_ylim((df_dp.min(), 0))
    ax5.set_ylabel("z [m]")
    
    #ax4.tricontour(df_dt, df_dp, df_do, 20, linewidths = 0.0, colors = 'k')
    cntr = ax4.tricontourf(df_dt, df_dp, df_do, 200, cmap = "jet")
    cb = plt.colorbar(cntr, ax=ax4)
    cb.locator = mpl.ticker.MaxNLocator(5)
    cb.update_ticks()
    cb.set_label('DO [mg/l]')
    formatter = dt.DateFormatter('%Y-%m')
    ax4.xaxis.set_major_formatter(formatter)
    ax4.set_ylim((df_dp.min(), 0))
    ax4.set_ylabel("z [m]")
    
    plt.tight_layout()
    
    if year_b == year_e:
        year = str(year_b)
    else:
        year = str(year_b) + "_" + str(year_e)
    fig.savefig("plot/Modified " + year + "_Chibatokyo_Station", dpi = 1200)
    
    return None

if __name__  == '__main__':
    path = "../data/monitoring_post/case_2014_2017";
    df = pickle.load(open(path+"/water.tkb", mode = "rb"))
    df = mod_col(df)
    for i in range(2014, 2017):
        j = i + 1
        df_year = choose_year(df, i, j)
        df_clean = prepare_data(df_year)
        df_alltime = uniform_time(df_clean, i, j)
        df_dt, df_dp, df_te, df_ch, df_sa, df_ss, df_do = make_array(df_clean)
        print("Generating the data plotting of " + str(i) + " ...")
        plot_values(df_dt, df_dp, df_te, df_ch, df_sa, df_ss, df_do, i, i)        
        pickle.dump(df_alltime, open("water_alltime_" + str(i) + "_to_" + str(j) + ".tkb", mode = "wb"), protocol = True)
        
        
        
        
        
        
        
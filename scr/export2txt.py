# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 06:46:25 2018
@author: Yulong Wang
"""
import pickle
import numpy as np
import pandas as pd
import datetime as dttm
import matplotlib.dates as dt
from datetime import datetime
import matplotlib.pyplot as plt

def io_year():
    print("Loading " + "water_alltime_2004_to_2017.tkb" + "...")
    year_b = input("Please enter your beginning year:\n")
    print("The beginning time is: " + year_b + "-01-01 00:00:00")
    year_e = input("Please enter your ending year:\n")
    print("The ending time is: " + year_e + "-12-31 23:00:00\n")
    hour = input("Please enter interval hour:\n")
    print("The ending time is: " + hour + "-12-31 23:00:00\n")
    year_b = int(year_b)
    year_e = int(year_e)
    hour = int(hour)
    return year_b, year_e, hour

def choose_year(df, year_b, year_e):
    df = df[df["YEAR"] >= int(year_b)]
    df = df[df["YEAR"] <= int(year_e)]
    return df

def uniform_time(df_sst, year_b, year_e, hour):
    date1 = dttm.datetime(year_b, 1, 1, 0, 0, 0, 0)
    date2 = dttm.datetime(year_e, 12, 31, 23, 0, 0, 0)
    delta = dttm.timedelta(hours = hour)
    dates = dt.drange(date1, date2, delta)
    dateframe = pd.DataFrame({"DATE & TIME":[], "uniform_time":[], "flag":[]})
    dateframe["uniform_time"] = [i for i in dates]
    dateframe["DATE & TIME"] = [i.strftime("%Y/%m/%d %H:%M:%S") for i in dt.num2date(dates)]
    dateframe["flag"] = [1 for i in dates]
    df_ut = dateframe.merge(df_sst, on = ["DATE & TIME"], how = "outer")
    df_ut = df_ut[df_ut["flag"] == 1]
    return df_ut

def generate_sst(df_year, year_b, year_e, hour):
    df_sst = df_year[df_year["SEQ_NO"] == 0]
    df_sst = uniform_time(df_sst, year_b, year_e, hour)
    df_sst.drop(["uniform_time_x","uniform_time_y","SEQ_NO","DEPTH(m.DL)",\
                 "Chl-a(ug/l)","SAL(psu)","SS(mg/l)","DO(%)","DO(mg/l)",\
                 "BOTTOM(m)","YEAR","flag"], axis = 1, inplace = True)
    return df_sst

def generate_xy(df_sst):
    sst = np.array([i for i in df_sst["TEMP(deg)"].interpolate()])
    time = np.array([dt.date2num(i) for i in (np.array([datetime.strptime(str(i), "%Y/%m/%d %H:%M:%S") for i in df_sst["DATE & TIME"]]))])
    time_p = np.array([i.strftime("%Y-%m-%d %H:%M:%S") for i in dt.num2date(time)])
    return sst, time, time_p

def plot_sst(hour, year, time, sst):

    g_ratio = (1. + np.sqrt(5.)) / 2.
    f_width = 7.48
    figsize = (f_width, f_width / g_ratio * 2 / 3)    
    fig, ax = plt.subplots(nrows = 1, figsize = figsize)
    fig.autofmt_xdate()
    ax.plot(time, sst)
    #plt.axis([0, 1, 1.1 * np.min(s), 2 * np.max(s)])
    plt.xlabel('time (s)')
    plt.ylabel('temperature (degC)')
    plt.title("Sea Surface Temperature change of " + year + ".")
    formatter = dt.DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim((time.min(), time.max()))
    fig.savefig("outputs/sst/" + "sst_per_" + str(hour) + "_" + year + ".png", dpi = 1200)
    return None

def write_sst(hour, year, time_p, sst):
    file = open("outputs/sst/" + "sst_per_" + str(hour) + "_" + year + ".txt", 'w+')
    i = 0
    while i < len(sst):
        print(time_p[i] + "   " + str("{:.2f}".format(sst[i])))
        file.write(time_p[i] + "   " + str("{:.3f}".format(sst[i])) + "\n")
        i = i + 1
    file.close()
    return None

##########
    
def interpolate_depth(df_time):
    #depth1 = df_time[0:1]["DEPTH(m.DL)"].tolist()[0]
    #depth2 = df_time[-2:-1]["DEPTH(m.DL)"].tolist()[0]
    depthframe = pd.DataFrame({"DEPTH(m.DL)":[], "flag":[]})
    depthframe["DEPTH(m.DL)"] = [k * -0.01 + 2 for k in range(1200)]
    depthframe["flag"] = [2 for i in range(len(depthframe))]
    df_id = depthframe.merge(df_time, on = ["DEPTH(m.DL)"], how = "outer")
    return df_id

def generate_pro(df_year, year_b, year_e, hour):
    dates = dt.drange(dttm.datetime(year_b, 1, 1, 0, 0, 0, 0), dttm.datetime(year_e, 12, 31, 23, 0, 0, 0), dttm.timedelta(hours = hour))
    timeaxis = [i.strftime("%Y/%m/%d %H:%M:%S") for i in dt.num2date(dates)]
    df_gt = pd.DataFrame({"DEPTH(m.DL)":[],"DATE & TIME":[],"TEMP(deg)":[],"Chl-a(ug/l)":[],"SAL(psu)":[],"SS(mg/l)":[],"DO(%)":[],"DO(mg/l)":[]})
    for i in timeaxis:
        df_time = df_year[df_year["DATE & TIME"] == i]
        df_id = interpolate_depth(df_time)
        df_id.drop(["uniform_time","SEQ_NO","BOTTOM(m)","YEAR","flag"], axis = 1, inplace = True)
        df_id["DATE & TIME"] = [i for j in range(len(df_id))]
        df_id.sort_values('DEPTH(m.DL)', inplace = True)
        df_id.reset_index(drop = True, inplace = True)
        df_id = df_id.interpolate()
        #df_id["TEMP(deg)"] = [i for i in df_id["TEMP(deg)"].interpolate()]
        #df_id["Chl-a(ug/l)"] = [i for i in df_id["Chl-a(ug/l)"].interpolate()]
        #df_id["SAL(psu)"] = [i for i in df_id["SAL(psu)"].interpolate()]
        #df_id["SS(mg/l)"] = [i for i in df_id["SS(mg/l)"].interpolate()]
        #df_id["DO(%)"] = [i for i in df_id["DO(%)"].interpolate()]
        #df_id["DO(mg/l)"] = [i for i in df_id["DO(mg/l)"].interpolate()]
        df_gt = pd.concat([df_gt, df_id], ignore_index = True)
    df_gt = df_gt.dropna(axis = 0, how = 'any')
    return df_gt

def make_frame():
    dates = dt.drange(dttm.datetime(year_b, 1, 1, 0, 0, 0, 0), dttm.datetime(year_e, 12, 31, 23, 0, 0, 0), dttm.timedelta(hours = hour))
    timeaxis = [i.strftime("%Y/%m/%d %H:%M:%S") for i in dt.num2date(dates)]
    df_mf = pd.DataFrame({"DEPTH(m.DL)":[],"DATE & TIME":[]})
    df_id = pd.DataFrame({"DEPTH(m.DL)":[],"DATE & TIME":[]})
    for i in timeaxis:
        df_id["DATE & TIME"] = [i for j in range(25)]
        df_id["DEPTH(m.DL)"] = [k * -0.5 + 2 for k in range(25)]
        df_mf = pd.concat([df_mf, df_id], ignore_index = True)
    return df_mf

def choose_depth(df_gt):
    df_cd = make_frame()
    df_data = df_gt[[round(i, 2) % 0.5 == 0 for i in df_gt[:]["DEPTH(m.DL)"]]]
    df_cd = df_cd.merge(df_data, on = ["DEPTH(m.DL)", "DATE & TIME"], how = "outer")
    #df_cd.reset_index(drop = True, inplace = True)
    return df_cd

def fix_missing(df_cd):
    timelist = sorted(set([i for i in df_cd["DATE & TIME"]]), reverse = False)
    linenumb = len(df_cd)/len(timelist)
    df_fm = pd.DataFrame({"DEPTH(m.DL)":[],"DATE & TIME":[],"TEMP(deg)":[],"Chl-a(ug/l)":[],"SAL(psu)":[],"SS(mg/l)":[],"DO(%)":[],"DO(mg/l)":[]})
    for i in range(int(linenumb)):
        df_fmd = df_cd.iloc[[i + j for j in range(0, len(df_cd), int(linenumb))]]
        df_fmd = df_fmd.interpolate()
        df_fm = pd.concat([df_fm, df_fmd], ignore_index = False)
        df_fm = df_fm.sort_index()
    return df_fm

def write_pro(df_fm, col_name, year, hour):
    if col_name == "TEMP(deg)":
        value = "tprof"
    if col_name == "Chl-a(ug/l)":
        value = "cprof"
    if col_name == "SAL(psu)":
        value = "sprof"
    if col_name == "SS(mg/l)":
        value = "ssprof"
    if col_name == "DO(mg/l)":
        value = "dprof"
    file = open("outputs/profile/" + value + "_" + str(hour) + "_" + year + ".txt", 'w+')
    i = 0
    while i < len(df_fm) / 25:
        print(df_fm[i * 25 : i * 25 + 1]["DATE & TIME"].tolist()[0].replace("/", "-") + "  24 2")
        file.write(df_fm[i * 25 : i * 25 + 1]["DATE & TIME"].tolist()[0].replace("/", "-") + "  24 2" + "\n")
        for j in range(24):
            print(" " + "{:.1f}".format(-0.5 * j + 2.0) + "  " + "{:.4f}".format(df_fm[i * 25 + j : i * 25 + j + 1][col_name].tolist()[0]))
            file.write(" " + "{:.1f}".format(-0.5 * j + 2.0) + "  " + "{:.4f}".format(df_fm[i * 25 + j : i * 25 + j + 1][col_name].tolist()[0]) + "\n")
        i = i + 1
    file.close()
    return None

if __name__  == '__main__':
    df = pickle.load(open("water_alltime_2004_to_2017.tkb", mode = "rb"))
    #year_b, year_e, hour = io_year()
    hour = 1
    for i in range(2004, 2005):
        year_b = i
        year_e = i
        df_year = choose_year(df, year_b, year_e)    
        if year_b == year_e:
            year = str(year_b)
        else:
            year = str(year_b) + " to " + str(year_e) 
########## SST.DAT GENERATOR ##########
#        df_sst = generate_sst(df_year, year_b, year_e, hour)
#        print("Generated " + str(len(df_sst)) + " lines, equivalent to " + str(len(df_sst) / 24 * hour) + " days.\n")
#        sst, time, time_p = generate_xy(df_sst)
#        plot_sst(hour, year, time, sst)
#        write_sst(hour, year, time_p, sst)
########## XPROF.DAT GENERATOR ##########    
        col_name = ["TEMP(deg)", "SAL(psu)","DO(mg/l)"]
        df_gt = generate_pro(df_year, year_b, year_e, hour)
        df_cd = choose_depth(df_gt)
        df_fm = fix_missing(df_cd)
        for col in col_name:
            write_pro(df_fm, col, year, hour)
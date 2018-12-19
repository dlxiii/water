# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 13:30:18 2018

@author: 8696690647
"""

import pickle
import datetime as dttm
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.dates as dt
from datetime import datetime
import matplotlib.pyplot as plt

def choose_year(df, year):
    df_cy = df[df["DATE & TIME"].str[0:4] == str(year)]
    return df_cy

def make_frame(df_cy):
    year_mf = int(df_cy["DATE & TIME"][0:1].str[0:4].values[0])
    datetimelist = dt.drange(dttm.datetime(year_mf, 1, 1, 0, 0, 0, 0), dttm.datetime(year_mf, 12, 31, 23, 0, 0, 0), dttm.timedelta(hours = 1))
    datetimelist = [i.strftime("%Y/%m/%d %H:%M:%S") for i in dt.num2date(datetimelist)]
    df_mf = pd.DataFrame({"DEPTH(m.DL)":[],"DATE & TIME":[],"STATUS":[]})
    miss = []
    for datetimevalue in datetimelist:
        df_val = df_cy[df_cy["DATE & TIME"] == datetimevalue]
        df_id = pd.DataFrame({"DEPTH(m.DL)":[],"DATE & TIME":[],"STATUS":[]})
        rownum = len(df_val)
        if rownum == 0:
            rownum = 10
            miss.append(datetimevalue)
            df_id["DEPTH(m.DL)"] = [-0.97 - row for row in range(rownum)]
            df_id["DATE & TIME"] = [datetimevalue for row in range(rownum)]
            df_id["STATUS"] = ["Added" for row in range(rownum)]
        else:
            df_id["DEPTH(m.DL)"] = [val for val in df_val["DEPTH(m.DL)"]]
            df_id["DATE & TIME"] = [datetimevalue for j in range(rownum)]
            df_id["STATUS"] = ["0" for row in range(rownum)]
        df_mf = pd.concat([df_mf, df_id], ignore_index = True)
    return df_mf, miss

def merge_data(df_mf, df_cy):
    df_md = df_mf.merge(df_cy, on = ["DATE & TIME", "DEPTH(m.DL)"], how = "outer")
    return df_md

def t_neighbour(time, datatimemiss):
    yer = int(time[0:4])
    mon = int(time[5:7])
    day = int(time[8:10])
    hor = int(time[11:13])
    time_current = dttm.datetime(yer, mon, day, hor, 0, 0, 0)
    time_foreward = time_current - dttm.timedelta(hours = 1)
    time_backward = time_current + dttm.timedelta(hours = 1)
    while time_foreward.strftime("%Y/%m/%d %H:%M:%S") in datatimemiss:
        time_foreward = time_foreward  - dttm.timedelta(hours = 1)
    while time_backward.strftime("%Y/%m/%d %H:%M:%S") in datatimemiss:
        time_backward = time_backward  + dttm.timedelta(hours = 1)
    return time_foreward.strftime("%Y/%m/%d %H:%M:%S"), time_backward.strftime("%Y/%m/%d %H:%M:%S")

def gener_value(df_md, time_nei_0, time_nei_1, time):
    df_nei_0 = df_md[df_md["DATE & TIME"] == time_nei_0]
    df_nei_1 = df_md[df_md["DATE & TIME"] == time_nei_1]
    df_curnt = df_md[df_md["DATE & TIME"] == time]
    df_depth = pd.DataFrame({"DEPTH(m.DL)":[],"STATUS_x":[]})
    df_depth["DEPTH(m.DL)"] = [i for i in df_curnt["DEPTH(m.DL)"]]
    df_depth["STATUS_x"] = ["1" for i in range(len(df_curnt))]
    df_new_0 = df_depth.merge(df_nei_0, on = ["DEPTH(m.DL)","STATUS_x"], how = "outer")
    df_new_1 = df_depth.merge(df_nei_1, on = ["DEPTH(m.DL)","STATUS_x"], how = "outer")
    df_new_0.sort_values("DEPTH(m.DL)", inplace=True, ascending = False)
    df_new_1.sort_values("DEPTH(m.DL)", inplace=True, ascending = False)
    targ_dep = sorted(set([i for i in df_curnt["DEPTH(m.DL)"]]), reverse = True)
    targ_dep_0 = df_new_0.interpolate()
    targ_dep_1 = df_new_1.interpolate()
    targ_dep_0 = targ_dep_0[targ_dep_0["STATUS_x"] == "1"]
    targ_dep_1 = targ_dep_1[targ_dep_1["STATUS_x"] == "1"]
    targ_dep_0["DATE & TIME"] = [time_nei_0 for i in range(len(targ_dep_0))]
    targ_dep_1["DATE & TIME"] = [time_nei_1 for i in range(len(targ_dep_1))]
    return targ_dep_0, targ_dep_1, targ_dep

def fix_missing(df_cy):
    df_mf, datetimemiss = make_frame(df_cy)
    df_md = merge_data(df_mf, df_cy)
    time_nei_list_0 = []
    time_nei_list_1 = []
    for time in datetimemiss:
        time_nei_0, time_nei_1 = t_neighbour(time, datetimemiss)
        time_nei_list_0.append(time_nei_0)
        time_nei_list_1.append(time_nei_1)
    time_nei_list_0 = sorted(set(time_nei_list_0))
    time_nei_list_1 = sorted(set(time_nei_list_1))
    time_saver = [(datetime.strptime(i, "%Y/%m/%d %H:%M:%S") + dttm.timedelta(hours = 1)).strftime("%Y/%m/%d %H:%M:%S") for i in time_nei_list_0]
    #time_gaps = [int((datetime.strptime(time_nei_list_1[i], "%Y/%m/%d %H:%M:%S") - datetime.strptime(time_nei_list_0[i], "%Y/%m/%d %H:%M:%S")) / dttm.timedelta(hours = 1) - 1) for i in range(len(time_saver))]
    df_fm = pd.DataFrame({"DEPTH(m.DL)":[],"DATE & TIME":[]})
    for i in range(len(time_nei_list_0)):
        targ_dep_0 = gener_value(df_md, time_nei_list_0[i], time_nei_list_1[i], time_saver[i])[0]
        targ_dep_1 = gener_value(df_md, time_nei_list_0[i], time_nei_list_1[i], time_saver[i])[1]
        df_md = pd.concat([df_md,targ_dep_0,targ_dep_1],axis=0,sort=False)
    df_md.sort_values(by = ["DATE & TIME","DEPTH(m.DL)"], inplace=True, ascending = True)
    df_md.reset_index(drop = True, inplace = True)
    df_md = df_md.drop(["STATUS_y"], axis=1)
    targ_dep = gener_value(df_md, time_nei_list_0[i], time_nei_list_1[i], time_saver[i])[2]
    df_fn = df_cy
    for i in targ_dep:
        df_fm = df_md[df_md["DEPTH(m.DL)"] == i]
        df_fm = df_fm.interpolate()
        df_fm = df_fm[df_fm["STATUS_x"] == "Added"]
        df_fm = df_fm[["DATE & TIME", "DEPTH(m.DL)","TEMP(deg)","Chl-a(ug/l)","SAL(psu)","SS(mg/l)","DO(%)","DO(mg/l)","BOTTOM(m)"]]
        df_fn = pd.concat([df_fn,df_fm], ignore_index = True,sort=False)
    df_fn = df_fn[["DATE & TIME", "DEPTH(m.DL)","TEMP(deg)","Chl-a(ug/l)","SAL(psu)","SS(mg/l)","DO(%)","DO(mg/l)","BOTTOM(m)"]]
    df_fn.sort_values(by = ["DATE & TIME","DEPTH(m.DL)"], inplace=True, ascending = False)
    df_fn.reset_index(drop = True, inplace = True)
    return df_fn

def choose_time(df_cy, value):
    df_ct = df_cy[df_cy["DATE & TIME"] == value]
    return df_ct

def write_val(col_name):
    if col_name == "TEMP(deg)":
        value = "tprof"
    if col_name == "SAL(psu)":
        value = "sprof"
    if col_name == "VELOCITY(cm/s)":
        value = "ext_press_prof"
    if col_name == "DO(mg/l)":
        value = "o2_prof"
    return value

def write_year(df_fn):
    yearlist = sorted(set([i[0:4] for i in df_fn["DATE & TIME"]]), reverse = False)
    if len(yearlist) == 1:
        year = yearlist[0]
    else:
        year = yearlist[0] + "_" + yearlist[-1]
    return year
    

def write_profile(df_fn, col_name):
    value = write_val(col_name)
    year = write_year(df_fn)
    timelist = sorted(set([i for i in df_fn["DATE & TIME"]]), reverse = False)
    file = open("outputs/profile/" + value + "_" + year + ".txt", 'w+')
    for datetimevalue in timelist:
        df_ct = choose_time(df_fn, datetimevalue)
        print(datetimevalue.replace("/", "-") + "{:4d}".format(len(df_ct)) + " 2")
        file.write(datetimevalue.replace("/", "-") + "{:4d}".format(len(df_ct)) + " 2" + "\n")
        for j in range(len(df_ct)):
           print(" " + "{:.2f}".format(df_ct["DEPTH(m.DL)"].tolist()[j]) + "  " + "{:.4f}".format(df_ct[col_name].tolist()[j]))
           file.write(" " + "{:.2f}".format(df_ct["DEPTH(m.DL)"].tolist()[j]) + "  " + "{:.4f}".format(df_ct[col_name].tolist()[j]) + "\n")
    file.close()
    return None

if __name__  == '__main__':
    df = pickle.load(open("water.tkb", mode = "rb"))
    yearlist = sorted(set([i[0:4] for i in df["DATE & TIME"]]), reverse = False)
    deptlist = sorted(set([i for i in df["DEPTH(m.DL)"]]), reverse = True)   
    for year in yearlist:
        df_cy = choose_year(df, year)
        df_fn = fix_missing(df_cy)
        write_profile(df_fn, "TEMP(deg)")
        write_profile(df_fn, "SAL(psu)")
        write_profile(df_fn, "DO(mg/l)")
    
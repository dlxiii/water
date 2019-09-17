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

def write_year(df_cy):
    yearlist = sorted(set([i[0:4] for i in df_cy["DATE & TIME"]]), reverse = False)
    if len(yearlist) == 1:
        year = yearlist[0]
    else:
        year = yearlist[0] + "_" + yearlist[-1]
    return year
    

def write_profile(df_cy, col_name):
    value = write_val(col_name)
    year = write_year(df_cy)
    timelist = sorted(set([i for i in df_cy["DATE & TIME"]]), reverse = False)
    file = open("outputs/profile/" + value + "_" + year + ".txt", 'w+')
    for datetimevalue in timelist:
        df_ct = choose_time(df_cy, datetimevalue)
        #print(datetimevalue.replace("/", "-") + "{:4d}".format(len(df_ct)) + " 3")
        #file.write(datetimevalue.replace("/", "-") + "{:4d}".format(len(df_ct)) + " 3" + "\n")
        #for j in range(len(df_ct)):
        for j in range(2,3):
           print(datetimevalue.replace("/", "-") + "  " + "{:.1f}".format(df_ct["DEPTH(m.DL)"].tolist()[j] + 10.6) + "  " + "{:.2e}".format(df_ct["V-E(cm/s)"].tolist()[j]/100.) + "  " + "{:.2e}".format(df_ct["V-N(cm/s)"].tolist()[j]/100.))
           file.write(datetimevalue.replace("/", "-") + "  " + "{:.1f}".format(df_ct["DEPTH(m.DL)"].tolist()[j] + 10.6) + "  " + "{:.2e}".format(df_ct["V-E(cm/s)"].tolist()[j]/100.) + "  " + "{:.2e}".format(df_ct["V-N(cm/s)"].tolist()[j]/100.) + "\n")
    file.close()
    return None

if __name__  == '__main__':
    df = pickle.load(open("currt.tkb", mode = "rb"))
    yearlist = sorted(set([i[0:4] for i in df["DATE & TIME"]]), reverse = False)
    deptlist = sorted(set([i for i in df["DEPTH(m.DL)"]]), reverse = True)   
    #for year in yearlist:
    for year in range(2004,2005):
        df_cy = choose_year(df, year)    
        write_profile(df_cy, "VELOCITY(cm/s)")
    
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 18:02:32 2019

@author: Yulong
"""

import pickle
import datetime as dttm
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.dates as dt
from datetime import datetime
import matplotlib.pyplot as plt

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

def wash_noise(df, col_name, num):
    df_te = df[(df[col_name] - df[col_name].mean()).abs() <= num * df[col_name].std()]
    print("There are " + str(len(df) - len(df_te)) + " lines of " + col_name + " data are dropped.")
    return df_te

def prepare_data(df):
    df = wash_noise(df, "TEMP(deg)", 3)
    df = wash_noise(df, "Chl-a(ug/l)", 30)
    df = wash_noise(df, "SAL(psu)", 15)
    df = wash_noise(df, "SS(mg/l)", 60)
    df = wash_noise(df, "DO(mg/l)", 6)
    return df

if __name__  == '__main__':
    # 读取数据
    path = "../data/monitoring_post/case_2014_2017";
    df = pickle.load(open(path+"/water.tkb", mode = "rb"))
    # 整理数据
    df = mod_col(df)
    # 去除噪音
    df_c = prepare_data(df)
    # 提取区间
    df_sf = df_c[df_c['SEQ_NO'] == 0]
    df_bt = df_c[df_c['DEPTH(m.DL)'] < -9.0]
    df_md = df_c[(df_c['DEPTH(m.DL)'] < -4.5) & (df_c['DEPTH(m.DL)'] > -5.5)]
    
    df_sf.to_csv(path+"/layers/water_surface.csv", sep=',', encoding = "utf-8");
    df_md.to_csv(path+"/layers/water_middle.csv", sep=',', encoding = "utf-8")
    df_bt.to_csv(path+"/layers/water_bottom.csv", sep=',', encoding = "utf-8")
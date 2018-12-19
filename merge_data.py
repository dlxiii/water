# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:54:20 2018
@author: Yulong Wang
"""

import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.tri as tri
from datetime import datetime
import matplotlib.pyplot as plt

def read_file(path, item, time):
    temp = pd.read_csv(path + item + "_" + time + ".csv", encoding = "utf-8")
    print("Reading " + item + "_" + time + ".csv ...")
    print("Loaded " + str(len(temp)) + " lines of data.")
    # data = pd.DataFrame({columns_name:[] for columns_name in temp.columns.values.tolist()})
    return temp
    
def merge_file(itemlist, timelist, f_period):
    path = "backup/"
#    namelist = [[item + time for time in timelist] for item in itemlist]
    df_wq = pd.concat([read_file(path, itemlist[1], time) for time in timelist], ignore_index = True)
    df_cu = pd.concat([read_file(path, itemlist[2], time) for time in timelist], ignore_index = True)
    df_wi = pd.concat([read_file(path, itemlist[0], time) for time in timelist], ignore_index = True)
    #df_wq.to_csv("water.csv", sep=',', encoding = "utf-8")
    pickle.dump(df_wq, open("water.tkb", mode = "wb"), protocol = True)
    #df_cu.to_csv("currt.csv", sep=',', encoding = "utf-8")
    pickle.dump(df_cu, open("currt.tkb", mode = "wb"), protocol = True)
    #df_wi.to_csv("winds.csv", sep=',', encoding = "utf-8")
    pickle.dump(df_wi, open("winds.tkb", mode = "wb"), protocol = True)
    print("water.tkb(" + str(len(df_wq)) + " lines), currt.tkb(" + str(len(df_cu)) + " lines) and winds.tkb(" + str(len(df_wi)) + " lines) have been exported.")
    return df_wq, df_cu, df_wi

if __name__  == '__main__':
    filelist = os.listdir("backup")
    itemlist = sorted(set([i[0:-22] for i in filelist]), reverse = True)
    timelist = sorted(set([i[-21:-4] for i in filelist]), reverse = False)
    f_period = [int(timelist[0][0:8]), int(timelist[-1][9:18])]
    merge_file(itemlist, timelist, f_period)
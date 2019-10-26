#!/usr/bin/env python
# coding: utf-8

import os
import pickle
import pandas as pd


def read_file(path, item, time):
    temp = pd.read_csv(path  + '/' + item + '_' + time + '.csv', encoding = 'utf-8', parse_dates=True)
    print("Reading " + item + "_" + time + ".csv ...")
    print("Loaded " + str(len(temp)) + " lines of data.")
    # data = pd.DataFrame({columns_name:[] for columns_name in temp.columns.values.tolist()})
    return temp


def merge_file(path, out, itemlist, timelist):
#    namelist = [[item + time for time in timelist] for item in itemlist]
    df_wq = pd.concat([read_file(path, itemlist[1], time) for time in timelist], ignore_index = True)
    df_cu = pd.concat([read_file(path, itemlist[2], time) for time in timelist], ignore_index = True)
    df_wi = pd.concat([read_file(path, itemlist[0], time) for time in timelist], ignore_index = True)
    df_wq.to_csv(out+"/water.csv", sep=',', encoding = "utf-8")
    pickle.dump(df_wq, open(out+"/water.tkb", mode = "wb"), protocol = True)
    df_cu.to_csv(out+"/currt.csv", sep=',', encoding = "utf-8")
    pickle.dump(df_cu, open(out+"/currt.tkb", mode = "wb"), protocol = True)
    df_wi.to_csv(out+"/winds.csv", sep=',', encoding = "utf-8")
    pickle.dump(df_wi, open(out+"/winds.tkb", mode = "wb"), protocol = True)
    print("water.tkb(" + str(len(df_wq)) + " lines), currt.tkb(" + str(len(df_cu)) + " lines) and winds.tkb(" + str(len(df_wi)) + " lines) have been exported.")
    # return df_wq, df_cu, df_wi

if __name__  == '__main__':
    # 定义文件位置
    path = "../data/monitoring_post/downloads";
    out = "../data/monitoring_post/preprocess";
    # 获取文件列表
    filelist = os.listdir(path)
    # 获取数据种类
    itemlist = sorted(set([i[0:-22] for i in filelist]), reverse = True)
    # 获取时间区间
    timelist = sorted(set([i[-21:-4] for i in filelist]), reverse = False)
    # 获取时间端点
    f_period = [int(timelist[0][0:8]), int(timelist[-1][9:18])]
    # 合并数据
    merge_file(path, out, itemlist, timelist)
    
    # 2014年到2017年数据提取到文件夹“case”
    timelist1 = ['20140101_20140228','20140301_20140430','20140501_20140630',\
                 '20140701_20140831','20140901_20141031','20141101_20141231',\
                 '20150101_20150228','20150301_20150430','20150501_20150630',\
                 '20150701_20150831','20150901_20151031','20151101_20151231',\
                 '20160101_20160229','20160301_20160430','20160501_20160630',\
                 '20160701_20160831','20160901_20161031','20161101_20161231',\
                 '20170101_20170228','20170301_20170430','20170501_20170630',\
                 '20170701_20170831','20170901_20171031','20171101_20171231',
                 '20180101_20180228'];
    out1 = "../data/monitoring_post/case_2014_2017";
    merge_file(path, out1, itemlist, timelist1);

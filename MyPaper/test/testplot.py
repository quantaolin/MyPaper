'''
Created on  2018-11-08 15:13:35

@author: quantaolin
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pymongo import MongoClient
import datetime

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.sb_set
test_sb_set = db.test_sb_set
test_result_set = db.test_result_set

dataDict={}
priceDict={}
for i in sb_set.find():
    code = i['code']
    collist = db.list_collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue   
    tmp_set = db[code]
    datalist = []
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        datalist.append(j['data'])
        pricelist.append(j['close'])
    dataDict[code]=datalist    
    priceDict[code]=pricelist

riseDict={}
fallDict={}

for i in test_result_set.find():
    code = i['code']
    print(code)
    riseAndFallFlag = i['riseAndFallFlag']
    index = i['index']
    useDict = fallDict
    if riseAndFallFlag == 1:
        useDict = riseDict       
    if code in useDict:
        useDict[code].append(index)
    else:
        useDict[code] = [index]

for i in test_sb_set.find():
    code = i['code']
    data = dataDict[code]
    value = priceDict[code]
    fmt = mdates.DateFormatter('%Y-%m-%d')
    timeArray = [datetime.datetime.strptime(i, '%Y-%m-%d') for i in data]
    a = np.array(timeArray)
    b = np.array(value)
    fig, ax = plt.subplots()
    plt.plot(a,b,'o-')
    ax.xaxis.set_major_formatter(fmt)
    plt.grid(True) ##增加格点
    plt.axis('tight')
    plt.title(i['code'][0:6])
    if code in riseDict:
        riseList = riseDict[code]
        for i in riseList:
            plt.annotate("⬆️", xy=(timeArray[i], value[i]), xytext=(-4, 3),
            textcoords='offset points'
            )
    if code in fallDict:
        fallList = fallDict[code]
        for i in fallList:
            plt.annotate("⬇️", xy=(timeArray[i], value[i]), xytext=(-4, 3),
            textcoords='offset points'
            )
    plt.show()       
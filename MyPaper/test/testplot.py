'''
Created on  2018-11-08 15:13:35

@author: quantaolin
'''
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.sb_set
test_result_set = db.test_result_set


priceDict={}
for i in sb_set.find():
    code = i['code']
    collist = db.list_collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue   
    tmp_set = db[code]
    pricederivatelist = []
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])       
    priceDict[code]=pricelist

riseDict={}
fallDict={}

for i in test_result_set.find():
    code = i['code']
    riseAndFallFlag = i['riseAndFallFlag']
    index = i['index']
    useDict = fallDict
    if riseAndFallFlag == 1:
        useDict = riseDict       
    if code in useDict:
        useDict[code].append(index)
    else:
        useDict[code] = [index]

for key,value in priceDict.items():
    b = np.array(value)
    plt.plot(b)
    plt.grid(True) ##增加格点
    plt.axis('tight')
    riseList = riseDict[key]
    for i in riseList:
        plt.annotate('上涨检测点：'+i+","+value[i], xy=(i, value[i]), xytext=(i+2, value[i]+2),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
    fallList = fallDict[key]
    for i in fallList:
        plt.annotate('下跌检测点：'+i+","+value[i], xy=(i, value[i]), xytext=(i+2, value[i]+2),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
    plt.show()       
'''
Created on  2018-11-01 17:35:37

@author: quantaolin
'''
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.sb_set
merge_rise_feature_set = db.merge_rise_feature_set
merge_fall_feature_set = db.merge_fall_feature_set

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
    
for i in merge_rise_feature_set.find():
    

for i in range(2):
    a = [1, 2, 5, 3, 4]
    b = np.array(a)
    plt.plot(b)
    plt.grid(True) ##增加格点
    plt.axis('tight')
    plt.show()

'''
Created on 2018-07-17 22:07

@author: linqt
'''
from pymongo import MongoClient

retracement_tolerance = 0.2
rebound_trend_confirm = 0.3

def getSubSeque(pricelist):
    last_min_index=0
    last_min_value=-1
    last_max_index=0
    last_max_value=-1
    riseandfall_flag=0
    key_point_indexs=[]
    key_point_riseandfall_flags=[]
    for index in range(len(pricelist)):
        value = pricelist[index]
        if index == 0: 
            last_min_value = last_max_value = value
            continue
        if value < last_min_value:
            last_min_index = index
            last_min_value = value
        elif value > last_max_value:
            last_max_index = index
            last_max_value = value
        if riseandfall_flag == 0:
            if (value - last_min_value)/last_min_value > rebound_trend_confirm:
                riseandfall_flag = 1
                key_point_indexs.append(last_min_index)
                key_point_riseandfall_flags.append(riseandfall_flag)
                last_max_index = index
                last_max_value = value
            if (last_max_value - value)/last_max_value > retracement_tolerance:
                riseandfall_flag = -1
                key_point_indexs.append(last_max_index)
                key_point_riseandfall_flags.append(riseandfall_flag)
                last_min_index = index
                last_min_value = value   
        elif riseandfall_flag > 0:
            if (last_max_value - value)/last_max_value > retracement_tolerance:
                riseandfall_flag = -1
                key_point_indexs.append(last_max_index)
                key_point_riseandfall_flags.append(riseandfall_flag)
                last_min_index = index
                last_min_value = value
        elif riseandfall_flag < 0:
            if (value - last_min_value)/last_min_value > rebound_trend_confirm:
                riseandfall_flag = 1
                key_point_indexs.append(last_min_index)
                key_point_riseandfall_flags.append(riseandfall_flag)
                last_max_index = index
                last_max_value = value
    return key_point_indexs,key_point_riseandfall_flags

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.train_sb_set
seq_set = db.seq_set

for i in sb_set.find():
    code = i['code']
    
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    print("get stock:",code," price subsequence")
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
        
    key_point_indexs,key_point_riseandfall_flags = getSubSeque(pricelist)
    seq_set.insert({"code":code,"key_point_indexs":key_point_indexs,"key_point_riseandfall_flags":key_point_riseandfall_flags})
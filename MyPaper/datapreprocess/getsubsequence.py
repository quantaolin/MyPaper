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
    key_point_indexs=[0]
    key_point_riseandfall_flags=[]
    for index in range(len(pricelist)):
        value = pricelist[index]
        if index == 0: 
            last_min_value = last_max_value = value
            continue
        if riseandfall_flag == 0:
            if value < last_min_value:
                last_min_index = index
                last_min_value = value
                riseandfall_flag = -1
                key_point_riseandfall_flags.append(riseandfall_flag)
            elif value > last_max_value:
                last_max_index = index
                last_max_value = value
                riseandfall_flag = 1
                key_point_riseandfall_flags.append(riseandfall_flag)          
        elif riseandfall_flag > 0:
            
        elif riseandfall_flag < 0:
            
    return key_point_indexs,key_point_riseandfall_flags

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.sb_set

for i in sb_set.find():
    code = i['code']
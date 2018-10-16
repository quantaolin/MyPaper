from pymongo import MongoClient
import tushare as ts
import time
'''
Created on 2018-07-07 09:17

@author: quantaolin
'''

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
 
sb_300_set = db.sb_300_set
sb = ts.get_hs300s()

for index,item in sb.iterrows():
    sb_300_set.insert({"code":item['code']})
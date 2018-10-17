from pymongo import MongoClient
import tushare as ts
import time
'''
Created on 2018-07-07 09:17

@author: quantaolin
'''

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
 
sb_SHSZ_set = db.sb_SHSZ_set
sb = ts.get_h_data("000001",start= "2018-04-01",end= '2018-07-06')

print(sb)
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
sbshtrain = ts.get_k_data("000001",start= "2003-01-01",end= '2012-12-31')
sbshtest = ts.get_k_data("000001",start= "2013-01-01",end= '2018-10-01')
sbsztrain = ts.get_k_data("399001",start= "2003-01-01",end= '2012-12-31')
sbsztest = ts.get_k_data("399001",start= "2013-01-01",end= '2018-10-01')

print(sbshtrain)
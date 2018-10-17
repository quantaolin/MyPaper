from pymongo import MongoClient
import tushare as ts
import time
'''
Created on 2018-07-07 09:17

@author: quantaolin
'''

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
 
trainset = db.train_sb_set
testset = db.test_sb_set
trainset.insert({"code":"000001train"})
trainset.insert({"code":"399001train"})
testset.insert({"code":"000001test"})
testset.insert({"code":"399001test"})

sbshtrain = ts.get_k_data("000001",start= "2003-01-01",end= '2012-12-31')
shtrain_set = db['000001train']
for indx,item in sbshtrain.iterrows():
        shtrain_set.insert({"data":item['date'],"open":item['open'],"close":item['close'],"volume":item['volume'],"high":item['high'],"low":item['low']})  
sbshtest = ts.get_k_data("000001",start= "2013-01-01",end= '2018-10-01')
shtest_set = db['000001test']
for indx,item in sbshtest.iterrows():
        shtest_set.insert({"data":item['date'],"open":item['open'],"close":item['close'],"volume":item['volume'],"high":item['high'],"low":item['low']}) 
sbsztrain = ts.get_k_data("399001",start= "2003-01-01",end= '2012-12-31')
sztrain_set = db['399001train']
for indx,item in sbsztrain.iterrows():
        sztrain_set.insert({"data":item['date'],"open":item['open'],"close":item['close'],"volume":item['volume'],"high":item['high'],"low":item['low']}) 
sbsztest = ts.get_k_data("399001",start= "2013-01-01",end= '2018-10-01')
sztest_set = db['399001test']
for indx,item in sbsztest.iterrows():
        sztest_set.insert({"data":item['date'],"open":item['open'],"close":item['close'],"volume":item['volume'],"high":item['high'],"low":item['low']}) 


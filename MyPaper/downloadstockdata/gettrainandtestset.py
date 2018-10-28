'''
Created on 2018-08-11 10:52

@author: quantaolin
'''
from pymongo import MongoClient
import time
import tushare as ts

RISE_TRAIN_START='2014-09-01'
RISE_TRAIN_END='2014-12-31'
RISE_TEST_START='2015-01-01'
RISE_TEST_END='2015-04-30'

FALL_TRAIN_START='2015-06-01'
FALL_TRAIN_END='2015-07-31'
FALL_TEST_START='2015-08-01'
FALL_TEST_END='2015-09-30'

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb

sb_set = db.sb_set
sb_50_set = db.sb_50_set
risetrainset = db.rise_train_sb_set
risetestset = db.rise_test_sb_set
falltrainset = db.fall_train_sb_set
falltestset = db.fall_test_sb_set

def getstock(code,traintestflag):
    print('start get stock of code:',code,',flag:',traintestflag)
    rise_start_time=''
    rise_end_time=''
    fall_start_time=''
    fall_end_time=''
    if traintestflag == 'train':
        rise_start_time=RISE_TRAIN_START
        rise_end_time=RISE_TRAIN_END
        fall_start_time=FALL_TRAIN_START
        fall_end_time=FALL_TRAIN_END
        risetrainset.insert_one({"code":code+traintestflag+'rise'})
        falltrainset.insert_one({"code":code+traintestflag+'fall'})
    elif traintestflag == 'test':
        rise_start_time=RISE_TEST_START
        rise_end_time=RISE_TEST_END
        fall_start_time=FALL_TEST_START
        fall_end_time=FALL_TEST_END
        risetestset.insert_one({"code":code+traintestflag+'rise'})
        falltestset.insert_one({"code":code+traintestflag+'fall'})
    else:
        return
    rise_tmp_set = db[code+traintestflag+'rise']
    fall_tmp_set = db[code+traintestflag+'fall']
    risedf=None
    falldf=None
    wait_time = 300
    while True:
        try:
            risedf = ts.get_k_data(code,start= rise_start_time,end= rise_end_time)
            falldf = ts.get_k_data(code,start= fall_start_time,end= fall_end_time)
        except:
            print("get fail ,wait....",wait_time,"sec")
            time.sleep(wait_time)
            continue
        else:
            break
    #4.insert mongodb
    print(risedf)
    print(falldf)
    for indx,item in risedf.iterrows():
        rise_tmp_set.insert_one({"data":item['date'],"open":item['open'],"close":item['close'],"volume":item['volume'],"high":item['high'],"low":item['low']})
    for indx,item in falldf.iterrows():
        fall_tmp_set.insert_one({"data":item['date'],"open":item['open'],"close":item['close'],"volume":item['volume'],"high":item['high'],"low":item['low']})  

for i in sb_50_set.find():
    code = i['code']
    collist = db.list_collection_names()
    if code in collist:
        print("code:",code," is already getted continue")
        continue
    getstock(code,'train')
    getstock(code,'test')
    sb_set.insert_one({"code":code+"trainrise"})
    sb_set.insert_one({"code":code+"trainfall"})
    sb_set.insert_one({"code":code+"testrise"})
    sb_set.insert_one({"code":code+"testfall"})
'''
Created on 2018-10-27 17:06

@author: linqt
'''
from pymongo import MongoClient

retracement_tolerance = -0.2
rebound_trend_confirm = 0.3

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
risetrainset = db.rise_train_sb_set
risetestset = db.rise_test_sb_set
falltrainset = db.fall_train_sb_set
falltestset = db.fall_test_sb_set

rise_set = db.rise_set
unrise_set = db.unrise_set
fall_set = db.fall_set
unfall_set = db.unfall_set
test_sb_set = db.test_sb_set

for i in risetrainset.find():
    code = i['code']   
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
    firstprice = pricelist[0]
    lastprice = pricelist[-1]
    derrivatives = (lastprice-firstprice)/firstprice
    if derrivatives>rebound_trend_confirm:
        rise_set.insert_one(({"code":code,"index_group":[[0,len(pricelist)-1]]}))
        unfall_set.insert_one(({"code":code,"index_group":[[0,len(pricelist)-1]]}))
    elif derrivatives<retracement_tolerance:
        fall_set.insert_one(({"code":code,"index_group":[[0,len(pricelist)-1]]}))
        unrise_set.insert_one(({"code":code,"index_group":[[0,len(pricelist)-1]]}))
        
for i in falltrainset.find():
    code = i['code']   
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
    firstprice = pricelist[0]
    lastprice = pricelist[-1]
    derrivatives = (lastprice-firstprice)/firstprice
    if derrivatives>rebound_trend_confirm:
        rise_set.insert_one(({"code":code,"index_group":[[0,len(pricelist)-1]]}))
        unfall_set.insert_one(({"code":code,"index_group":[[0,len(pricelist)-1]]}))
    elif derrivatives<retracement_tolerance:
        fall_set.insert_one(({"code":code,"index_group":[[0,len(pricelist)-1]]}))
        unrise_set.insert_one(({"code":code,"index_group":[[0,len(pricelist)-1]]}))
        
for i in risetestset.find():
    code = i['code']   
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
    firstprice = pricelist[0]
    lastprice = pricelist[-1]
    derrivatives = (lastprice-firstprice)/firstprice
    if derrivatives<retracement_tolerance:
        risetestset.find_one_and_delete({"code":code})
        falltestset.insert_one({"code":code})
        test_sb_set.insert_one({"code":code})
    elif derrivatives>rebound_trend_confirm:
        test_sb_set.insert_one({"code":code})
    else:
        risetestset.find_one_and_delete({"code":code})
        
for i in falltestset.find():
    code = i['code']   
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
    firstprice = pricelist[0]
    lastprice = pricelist[-1]
    derrivatives = (lastprice-firstprice)/firstprice
    if derrivatives>rebound_trend_confirm:
        falltestset.find_one_and_delete({"code":code})
        risetestset.insert_one({"code":code})
        test_sb_set.insert_one({"code":code})
    elif derrivatives<retracement_tolerance:
        test_sb_set.insert_one({"code":code})
    else:
        falltestset.find_one_and_delete({"code":code})
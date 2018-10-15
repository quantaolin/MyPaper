'''
Created on 2018-07-16 21:58

@author: linqt
'''
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.sb_set

for i in sb_set.find():
    
    code = i['code']
    
    collist = db.list_collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    
    tmp_set = db[code]
    lastprice = 0   
    for j in tmp_set.find().sort("data"):
        if lastprice == 0:
            lastprice = j['close']
            tmp_set.update_one({"data":j['data']},{"$set":{"derivative":0}})
            continue
        derivative = (j['close'] - lastprice)/lastprice
        tmp_set.update_one({"data":j['data']},{"$set":{"derivative":derivative}})
        lastprice = j['close']  
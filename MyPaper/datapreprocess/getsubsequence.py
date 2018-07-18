'''
Created on 2018-07-17 22:07

@author: linqt
'''
from pymongo import MongoClient

retracement_tolerance = 0.2
rebound_trend_confirm = 0.3

def getSubSeque(pricelist):
    return

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.sb_set

for i in sb_set.find():
    code = i['code']
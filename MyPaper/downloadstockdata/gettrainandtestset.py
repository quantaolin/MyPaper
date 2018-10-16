'''
Created on 2018-08-11 10:52

@author: quantaolin
'''
from pymongo import MongoClient

TRAIN_PERCENT=0.5

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb

sb_set = db.sb_300_set
trainset = db.train_sb_set
testset = db.test_sb_set

sb_count = sb_set.find().count()
traincount = sb_count*TRAIN_PERCENT

index = 1

for i in sb_set.find():
    if index < traincount:
        trainset.insert(i)
    else:
        testset.insert(i)
    index += 1
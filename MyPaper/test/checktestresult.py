'''
Created on  2018-11-01 17:35:51

@author: quantaolin
'''
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.test_sb_set
test_result_set = db.test_result_set
risetestset = db.rise_test_sb_set
falltestset = db.fall_test_sb_set

rise_right=0
rise_wrong=0
fall_right=0
fall_wrong=0


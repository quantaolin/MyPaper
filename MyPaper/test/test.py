'''
Created on 2018-08-11 23:41

@author: quantaolin
'''
from pymongo import MongoClient
import math
import dataprocess.subsequencedtw

DTW_DISTANCE_THRESHOLD=10

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.test_sb_set
rise_feature_set = db.rise_feature_set
fall_feature_set = db.fall_feature_set
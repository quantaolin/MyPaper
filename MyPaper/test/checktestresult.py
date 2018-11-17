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
rise_feature_set = db.merge_rise_feature_set
fall_feature_set = db.merge_fall_feature_set

risefeaturecount=0
fallfeaturecount=0
for i in rise_feature_set.find():
    risefeaturecount += 1
for i in fall_feature_set.find():
    fallfeaturecount += 1

rise_right=0
rise_wrong=0
fall_right=0
fall_wrong=0

for i in test_result_set.find():
    code = i['code']
    riseAndFallFlag = i['riseAndFallFlag']
    if riseAndFallFlag == 1:
        re = risetestset.find_one({"code":code})
        if re is None:
            rise_wrong += 1
        else:
            rise_right += 1
    else:
        re = falltestset.find_one({"code":code})
        if re is None:
            fall_wrong += 1
        else:
            fall_right += 1     
print("rise feature count=",risefeaturecount,"rise total=",rise_right+rise_wrong,",right=",rise_right,",wrong=",rise_wrong,",accuracy＝",rise_right/(rise_right+rise_wrong))
print("fall feature count=",fallfeaturecount,"fall total=",fall_right+fall_wrong,",right=",fall_right,",wrong=",fall_wrong,",accuracy＝",fall_right/(fall_right+fall_wrong))
'''
Created on  2018-10-25 20:54:50

@author: quantaolin
'''
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
rise_feature_set = db.rise_feature_set
fall_feature_set = db.fall_feature_set
merge_rise_feature_set = db.merge_rise_feature_set
merge_fall_feature_set = db.merge_fall_feature_set

def getMaxGain(gainlist):
    mainGain = 0
    index = 0
    for i in range(gainlist):
        if gainlist[i] > mainGain:
            mainGain = gainlist[i]
            index = i
    return index

def mergeFeatureGroup(featuregroup,gaingroup):
    tmpFeatureGroup = []
    tmpGainGroup = []
    resultFeatureGroup = []
    resultGainGroup = []
    for i in range(featuregroup):
        feture = featuregroup[i]
        if len(tmpFeatureGroup) == 0:
            tmpFeatureGroup.append(feture)
            tmpGainGroup.append(gaingroup[i])
        else:
            if feture[0]-tmpFeatureGroup[-1][0] < 5:
                tmpFeatureGroup.append(feture)
                tmpGainGroup.append(gaingroup[i])
            else:
                index = getMaxGain(tmpGainGroup)
                resultFeatureGroup.append(tmpFeatureGroup[index])
                resultGainGroup.append(tmpGainGroup[index])
                tmpFeatureGroup.clear()
                tmpGainGroup.clear()
    return resultFeatureGroup,resultGainGroup

for i in rise_feature_set.find():
    code = i['code']
    featuregroup = i['featuregroup']
    gaingroup = i['gaingroup']
    resultFeatureGroup,resultGainGroup = mergeFeatureGroup(featuregroup,gaingroup)
    merge_rise_feature_set.insert_one({"code":code,"featuregroup":resultFeatureGroup,"gaingroup":resultGainGroup})
    
for i in fall_feature_set.find():
    code = i['code']
    featuregroup = i['featuregroup']
    gaingroup = i['gaingroup']
    resultFeatureGroup,resultGainGroup = mergeFeatureGroup(featuregroup,gaingroup)
    merge_fall_feature_set.insert_one({"code":code,"featuregroup":resultFeatureGroup,"gaingroup":resultGainGroup})
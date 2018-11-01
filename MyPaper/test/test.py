'''
Created on 2018-08-11 23:41

@author: quantaolin
'''
from pymongo import MongoClient
from dataprocess import subsequencedtw

DTW_DISTANCE_THRESHOLD=150

def getResult(featurePriceSeq,testPriceSeq,riseAndFallFlag,code):
    distanceMatrix = subsequencedtw.getDistanceMatrix(featurePriceSeq, testPriceSeq)
    lenx = len(featurePriceSeq)
    leny = len(testPriceSeq)
    costMatrix = subsequencedtw.getCostMatrix(distanceMatrix,lenx,leny)
    endCost = costMatrix[lenx-1]
    for i in range(1,leny):
        if endCost[i] < DTW_DISTANCE_THRESHOLD:
            print("for code:",code,"this is feature index:",i-1,",flag:",riseAndFallFlag)
            test_result_set.insert_one({"code":code,"riseAndFallFlag":riseAndFallFlag,"index":i-1})

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.test_sb_set
test_result_set = db.test_result_set
all_sb_set = db.shsz_sb_set
rise_feature_set = db.merge_rise_feature_set
fall_feature_set = db.merge_fall_feature_set

print("get price list")
pricederivatDict={}
priceDict={}
for i in all_sb_set.find():
    code = i['code']
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue   
    tmp_set = db[code]
    pricederivatlist = [] 
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricederivatlist.append(j['derivative'])
        pricelist.append(j['close'])      
    pricederivatDict[code]=pricederivatlist
    priceDict[code]=pricelist
    
print("get feature set")
riseFeatureDict={}
fallFeatureDict={}
for i in rise_feature_set.find():
    riseFeatureDict[i['code']]=i['featuregroup']
for i in fall_feature_set.find():
    fallFeatureDict[i['code']]=i['featuregroup']

print("deal test data")
for i in sb_set.find():
    code = i['code']
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    testPriceSeq = pricederivatDict[code]
    for key,value in riseFeatureDict.items():
        print("begin matching feature,code:",code,",featurecode:",key,",riseandfallflag:",1,",index:",value)
        for indexGroup in value:
            featurePriceSeq = pricederivatDict[key][indexGroup[0]:indexGroup[1]]
            getResult(featurePriceSeq,testPriceSeq,1,code)
        
    for key,value in fallFeatureDict.items():
        print("begin matching feature,code:",code,",featurecode:",key,",riseandfallflag:",-1,",index:",value)
        for indexGroup in value:
            featurePriceSeq = pricederivatDict[key][indexGroup[0]:indexGroup[1]]
            getResult(featurePriceSeq,testPriceSeq,-1,code)
        

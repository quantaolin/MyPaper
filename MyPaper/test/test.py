'''
Created on 2018-08-11 23:41

@author: quantaolin
'''
from pymongo import MongoClient
from dataprocess import subsequencedtw

DTW_DISTANCE_THRESHOLD=200
retracement_tolerance = 0.2
rebound_trend_confirm = 0.3
SEQ_MAX_LEN=20

def getResult(featurePriceSeq,testPriceSeq,riseAndFallFlag,code):
    costMatrix = subsequencedtw.getCostMatrix(featurePriceSeq, testPriceSeq)
    xIndex = len(featurePriceSeq) - 1
    maxY = len(testPriceSeq) - 1
    minY = xIndex
    if minY > maxY:
        minY = maxY
    for i in range(minY,maxY + 1):
        yIndexStart = 0
        if i > (SEQ_MAX_LEN-1):
            yIndexStart = i-SEQ_MAX_LEN+1
        tmpDist,tmpPath = subsequencedtw.getDtw(costMatrix,xIndex,i,yIndexStart)
        if tmpDist < DTW_DISTANCE_THRESHOLD:
            print("for code:",code,"this is feature index:",maxY-i,",flag:",riseAndFallFlag)
            test_result_set.insert({"code":code,"riseAndFallFlag":riseAndFallFlag,"index":maxY-i})

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.test_sb_set
test_result_set = db.test_result_set
all_sb_set = db.shsz_sb_set
rise_feature_set = db.rise_feature_set
fall_feature_set = db.fall_feature_set

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
        

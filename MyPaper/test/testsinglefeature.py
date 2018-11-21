'''
Created on  2018-11-21 14:29:25

@author: quantaolin
'''
from pymongo import MongoClient
from dataprocess import subsequencedtw
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

RISE_DTW_DISTANCE_THRESHOLD=90
FALL_DTW_DISTANCE_THRESHOLD=520


conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.sb_set
test_sb_set = db.test_sb_set
risetestset = db.rise_test_sb_set
falltestset = db.fall_test_sb_set
merge_rise_feature_set = db.merge_rise_feature_set
merge_fall_feature_set = db.merge_fall_feature_set

def getMatchCount(featurePriceSeq,testPriceSeq,DTW_DISTANCE_THRESHOLD):
    distanceMatrix = subsequencedtw.getDistanceMatrix(featurePriceSeq, testPriceSeq)
    lenx = len(featurePriceSeq)
    leny = len(testPriceSeq)
    costMatrix = subsequencedtw.getCostMatrix(distanceMatrix,lenx,leny)
    endCost = costMatrix[lenx-1]
    count=0
    for i in range(1,leny):
        if endCost[i] < DTW_DISTANCE_THRESHOLD:
            count+=1
    return count   


print("get price list")
pricederivatDict={}
priceDict={}
for i in sb_set.find():
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
    
for i in merge_rise_feature_set.find():
    featurecode=i['code']
    for indexGroup in i['featuregroup']:
        featurePriceSeq = pricederivatDict[featurecode][indexGroup[0]:indexGroup[1]]
        right=0
        wrong=0
        for j in test_sb_set.find():
            testcode=j['code']
            testPriceSeq = pricederivatDict[testcode]
            re = risetestset.find_one({"code":testcode})
            count = getMatchCount(featurePriceSeq,testPriceSeq,RISE_DTW_DISTANCE_THRESHOLD)
            if re is not None:
                right += count
            else:
                wrong += count
        if (right+wrong) == 0:
            continue
        print("feature code:",featurecode,",total count:",right+wrong,",right count:",right,",wrong count:",wrong,",accuracy:",right/(right+wrong))    
        pricelist = priceDict[featurecode]
        featurequeue = pricelist[indexGroup[0]:indexGroup[1]+1]
        b = np.array(featurequeue)
        plt.plot(b)
        plt.grid(True) ##增加格点
        plt.axis('tight')
        plt.title(featurecode[0:6] + "rise")
        plt.show()
    
    
for i in merge_fall_feature_set.find():
    code=i['code']
    for indexGroup in i['featuregroup']:
        featurePriceSeq = pricederivatDict[code][indexGroup[0]:indexGroup[1]]
        right=0
        wrong=0
        for j in test_sb_set.find():
            testcode=j['code']
            testPriceSeq = pricederivatDict[testcode]
            re = falltestset.find_one({"code":testcode})
            count = getMatchCount(featurePriceSeq,testPriceSeq,RISE_DTW_DISTANCE_THRESHOLD)
            if re is not None:
                right += count
            else:
                wrong += count
        if (right+wrong) == 0:
            continue
        print("feature code:",featurecode,",total count:",right+wrong,",right count:",right,",wrong count:",wrong,",accuracy:",right/(right+wrong))
        pricelist = priceDict[code]
        featurequeue = pricelist[indexGroup[0]:indexGroup[1]+1]
        b = np.array(featurequeue)
        plt.plot(b)
        plt.grid(True) ##增加格点
        plt.axis('tight')
        plt.title(featurecode[0:6] + 'fall')
        plt.show()    
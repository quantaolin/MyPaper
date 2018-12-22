'''
Created on 2018-10-27 17:06

@author: linqt
'''
from pymongo import MongoClient

retracement_tolerance = -0.2
rebound_trend_confirm = 0.3
minDintance = 20

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
risetrainset = db.rise_train_sb_set
risetestset = db.rise_test_sb_set
falltrainset = db.fall_train_sb_set
falltestset = db.fall_test_sb_set

rise_set = db.rise_set
unrise_set = db.unrise_set
fall_set = db.fall_set
unfall_set = db.unfall_set
test_sb_set = db.test_sb_set

def getseqandtag(pricelist):
    indexList = []
    for i in range(len(pricelist)):
        indexList.append(i)
    indexGroupList=[]
    tagList=[]
    while indexList:
        maxIndex,minIndex = getMaxAndMin(pricelist,indexList)
        tmpIndexList=[]
        tagList=[]
        if abs(maxIndex-minIndex) < minDintance:
            if maxIndex > minIndex:
                tmpIndexList.append([minIndex,maxIndex])
            else :
                tmpIndexList.append([maxIndex,minIndex])
            indexList = delIndex(indexList,tmpIndexList)
            continue
        try:
            if maxIndex > minIndex:
                tmpIndexList,tmpTagList=checkRise(pricelist,minIndex,maxIndex)
            elif maxIndex < minIndex:
                tmpIndexList,tmpTagList=checkFall(pricelist,maxIndex,minIndex)
            indexGroupList.extend(tmpIndexList)
            tagList.extend(tmpTagList)
        except:
            if maxIndex > minIndex:
                tmpIndexList.append([minIndex,maxIndex])
            else :
                tmpIndexList.append([maxIndex,minIndex])
        indexList = delIndex(indexList,tmpIndexList)
    return indexGroupList,tagList                  

def checkRise(pricelist,minIndex,maxIndex):
    if (pricelist[maxIndex]-pricelist[minIndex])/pricelist[minIndex]>rebound_trend_confirm:
        return [[minIndex,maxIndex]],[1]
    else :
        raise Exception("no")
    
def checkFall(pricelist,maxIndex,minIndex):
    if (pricelist[minIndex]-pricelist[maxIndex])/pricelist[maxIndex]<retracement_tolerance:
        return [[maxIndex,minIndex]],[-1]
    else :
        raise Exception("no")

def delIndex(indexList,tmpIndexList):
    for i in tmpIndexList:
        tmpList = indexList[0:indexList.index(i[0])]
        tmpList.extend(indexList[indexList.index(i[1])+1])
        indexList = tmpList
    return indexList

def getMaxAndMin(pricelist,indexList):
    maxValue = minValue = pricelist[indexList[0]]
    maxIndex = minIndex = indexList[0]
    for i in indexList:
        value = pricelist[i]
        if value > maxValue:
            maxValue = value
            maxIndex = indexList[i]
        if value < minValue:
            minValue = value
            minIndex = indexList[i]
    return maxIndex,minIndex
         

for i in risetrainset.find():
    code = i['code']   
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
    indexGroupList,tagList = getseqandtag(pricelist)
    for i in range(len(indexGroupList)):
        indexGroup=indexGroupList[i]
        tag=tagList[i]
    if tag>0:
        rise_set.insert_one(({"code":code,"index_group":indexGroup}))
        unfall_set.insert_one(({"code":code,"index_group":indexGroup}))
    elif tag<0:
        fall_set.insert_one(({"code":code,"index_group":indexGroup}))
        unrise_set.insert_one(({"code":code,"index_group":indexGroup}))
        
for i in falltrainset.find():
    code = i['code']   
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
    indexGroupList,tagList = getseqandtag(pricelist)
    for i in range(len(indexGroupList)):
        indexGroup=indexGroupList[i]
        tag=tagList[i]
    if tag>0:
        rise_set.insert_one(({"code":code,"index_group":indexGroup}))
        unfall_set.insert_one(({"code":code,"index_group":indexGroup}))
    elif tag<0:
        fall_set.insert_one(({"code":code,"index_group":indexGroup}))
        unrise_set.insert_one(({"code":code,"index_group":indexGroup}))
        
for i in risetestset.find():
    code = i['code']   
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
    firstprice = pricelist[0]
    lastprice = pricelist[-1]
    derrivatives = (lastprice-firstprice)/firstprice
    if derrivatives<retracement_tolerance:
        risetestset.find_one_and_delete({"code":code})
        falltestset.insert_one({"code":code})
        test_sb_set.insert_one({"code":code})
    elif derrivatives>rebound_trend_confirm:
        test_sb_set.insert_one({"code":code})
    else:
        risetestset.find_one_and_delete({"code":code})
        
for i in falltestset.find():
    code = i['code']   
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
    firstprice = pricelist[0]
    lastprice = pricelist[-1]
    derrivatives = (lastprice-firstprice)/firstprice
    if derrivatives>rebound_trend_confirm:
        falltestset.find_one_and_delete({"code":code})
        risetestset.insert_one({"code":code})
        test_sb_set.insert_one({"code":code})
    elif derrivatives<retracement_tolerance:
        test_sb_set.insert_one({"code":code})
    else:
        falltestset.find_one_and_delete({"code":code})
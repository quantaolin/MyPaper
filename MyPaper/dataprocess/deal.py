'''
Created on 2018-07-07 09:17

@author: quantaolin
'''
from pymongo import MongoClient
import math
import subsequencedtw

GAIN_THRESHOLD=0.5
DTW_DISTANCE_THRESHOLD=10
SEQ_MIN_LEN=5
SEQ_MAX_LEN=20

def getentropybyset(aset,bset):
    acount=0
    bcount=0
    for a in aset.find():
        aseq = a["index_group"]
        acount += len(aseq)
    for b in bset.find():
        bseq = b["index_group"]
        bcount += len(bseq)
    pa = acount/(acount+bcount)
    pb = bcount/(acount+bcount)
    return -pa*math.log(pa,2)-pb*math.log(pb,2)

def getseqentropy(queryseq,trueDict,falseDict,pricederivatDict):
    true_to_true_count=0
    true_to_false_count=0
    false_to_true_count=0
    false_to_false_count=0
    for key,value in trueDict.items():   
        pricederivatList = pricederivatDict[key]
        for indexgroup in value:
            mainpriceseq = pricederivatList[indexgroup[0],indexgroup[1]+1]
            dist, path = subsequencedtw.deal(queryseq, mainpriceseq)
            print("true dist:",dist,"code:",key,",startindex:",indexgroup[0],",endindex:",indexgroup[1])
            if dist <= DTW_DISTANCE_THRESHOLD:
                true_to_true_count += 1
            else:
                true_to_false_count += 1 
    for key,value in falseDict.items():
        pricederivatList = pricederivatDict[key]
        for indexgroup in value:
            mainpriceseq = pricederivatList[indexgroup[0],indexgroup[1]+1]
            dist, cost, path = subsequencedtw.deal(queryseq, mainpriceseq)
            print("true dist:",dist,"code:",key,",startindex:",indexgroup[0],",endindex:",indexgroup[1])
            if dist <= DTW_DISTANCE_THRESHOLD:
                false_to_true_count += 1
            else:
                false_to_false_count += 1
    totalcount=true_to_true_count+true_to_false_count+false_to_true_count+false_to_false_count
    ft=(true_to_true_count+false_to_true_count)/totalcount
    ff=(true_to_false_count+false_to_false_count)/totalcount
    pta=true_to_true_count/(true_to_true_count+false_to_true_count)
    ptb=false_to_true_count/(true_to_true_count+false_to_true_count)
    i1= -pta*math.log(pta,2)-ptb*math.log(ptb,2)
    pfa=true_to_false_count/(true_to_false_count+false_to_false_count)
    pfb=false_to_false_count/(true_to_false_count+false_to_false_count)
    i2= -pfa*math.log(pfa,2)-pfb*math.log(pfb,2)
    return ft*i1+ff*i2

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.train_sb_set
rise_set = db.rise_set
unrise_set = db.unrise_set
fall_set = db.fall_set
unfall_set = db.unfall_set
rise_feature_set = db.rise_feature_set
fall_feature_set = db.fall_feature_set

riseDict={}
unriseDict={}
fallDict={}
unfallDict={}
pricederivatDict={}
riseGroupEntropy=getentropybyset(rise_set,unrise_set)
print("get rise entropy:",riseGroupEntropy)
fallGroupEntropy=getentropybyset(fall_set,unfall_set)
print("get fall entropy:",fallGroupEntropy)

print("get rise dict")
for i in rise_set.find():
    riseDict[i['code']]=i['index_group']
print("get unrise dict")
for i in unrise_set.find():
    unriseDict[i['code']]=i['index_group']
print("get fall dict")
for i in fall_set.find():
    fallDict[i['code']]=i['index_group']
print("get unfall dict")
for i in unfall_set.find():
    unfallDict[i['code']]=i['index_group']
print("get price list")
for i in sb_set.find():
    code = i['code']
    collist = db.list_collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue   
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        print(code,j)
        pricelist.append(j['derivative'])       
    pricederivatDict[code]=pricelist

print("del rise")  
for key,value in riseDict.items():
    pricederivatList = pricederivatDict[key]
    print("del stock:",key)
    for indexgroup in value:
        startindex=indexgroup[0]
        endindex=indexgroup[1]
        for len in range(SEQ_MIN_LEN,SEQ_MAX_LEN+1):
            if len > (endindex-startindex+1):
                break
            for offset in range(endindex-startindex+1-len+1):
                print("get stock:",key,"begin,startindex:",startindex,",endindex:",endindex,",len:",len,",offset:",offset)
                queryseq=pricederivatList[startindex+offset,startindex+offset+len]
                print("queryseq:",queryseq)
                seqentropy=getseqentropy(queryseq,riseDict,unriseDict,pricederivatDict)
                gain=riseGroupEntropy-seqentropy
                print("seqentropy:",seqentropy,"gain:",gain)
                if gain >= GAIN_THRESHOLD:
                    print("get stock:",key,"begin,startindex:",startindex+offset,",endindex:",startindex+offset+len-1)
                    rise_feature_set.insert({"code":key,"startindex":startindex+offset,"endindex":startindex+offset+len-1})
                    
print("del fall")                     
for key,value in fallDict.items():
    pricederivatList = pricederivatDict[key]
    print("del stock:",key)
    for indexgroup in value:
        startindex=indexgroup[0]
        endindex=indexgroup[1]
        for len in range(SEQ_MIN_LEN,SEQ_MAX_LEN+1):
            if len > (endindex-startindex+1):
                break
            for offset in range(endindex-startindex+1-len+1):
                print("get stock:",key,"begin,startindex:",startindex,",endindex:",endindex,",len:",len,",offset:",offset)
                queryseq=pricederivatList[startindex+offset,startindex+offset+len]
                print("queryseq:",queryseq)
                seqentropy=getseqentropy(queryseq,fallDict,unfallDict,pricederivatDict)
                gain=fallGroupEntropy-seqentropy
                print("seqentropy:",seqentropy,"gain:",gain)
                if gain >= GAIN_THRESHOLD:
                    print("get stock:",key,"success,startindex:",startindex+offset,",endindex:",startindex+offset+len-1)
                    fall_feature_set.insert({"code":key,"startindex":startindex+offset,"endindex":startindex+offset+len-1})
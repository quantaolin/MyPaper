'''
Created on 2018-07-07 09:17

@author: quantaolin
'''
from pymongo import MongoClient
import math
import subsequencedtw

GAIN_THRESHOLD=0.5
RISE_DTW_DISTANCE_THRESHOLD=90
FALL_DTW_DISTANCE_THRESHOLD=520
SEQ_MIN_LEN=20
SEQ_MAX_LEN=20 

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
subdtw_result_set = db.subdtw_result_set

def saveSubDtw(queryCode,queryStartIndex,queryEndIndex,majorCode,majorStartIndex,majorEndIndex,dist,offset):
    subdtw_result_set.insert_one({"querycode":queryCode,"querystartindex":queryStartIndex,"queryendindex":queryEndIndex,"majorcode":majorCode,
                             "majorstartindex":majorStartIndex,"majorendindex":majorEndIndex,"dist":dist,"offset":offset})

def querySubDtw(queryCode,queryStartIndex,queryEndIndex,majorCode,majorStartIndex,majorEndIndex):
    re = subdtw_result_set.find_one({"querycode":queryCode,"querystartindex":queryStartIndex,"queryendindex":queryEndIndex,"majorcode":majorCode,
                             "majorstartindex":majorStartIndex,"majorendindex":majorEndIndex})
    if re is None:
        return None,None
    return re['dist'],re['offset']

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

def getseqentropy(queryseq,trueDict,falseDict,pricederivatDict,queryCode,queryStartIndex,queryEndIndex,risefallflag):
    DTW_DISTANCE_THRESHOLD=RISE_DTW_DISTANCE_THRESHOLD
    if risefallflag == 'fall':
        DTW_DISTANCE_THRESHOLD=FALL_DTW_DISTANCE_THRESHOLD
    true_to_true_count=0
    true_to_false_count=0
    false_to_true_count=0
    false_to_false_count=0
    for key,value in trueDict.items():   
        pricederivatList = pricederivatDict[key]
        for indexgroup in value:
            mainpriceseq = pricederivatList[indexgroup[0]:indexgroup[1]+1]
            dist, offset = subsequencedtw.subDtw(queryseq, mainpriceseq)
#             dist, offset = querySubDtw(queryCode,queryStartIndex,queryEndIndex,key,indexgroup[0],indexgroup[1])
#             if dist == None:
#                 dist, offset = subsequencedtw.subDtw(queryseq, mainpriceseq)
#                 saveSubDtw(queryCode,queryStartIndex,queryEndIndex,key,indexgroup[0],indexgroup[1],dist,offset)
#             if risefallflag == 'fall':
#                 print("true dist:",dist,"code:",key,",startindex:",indexgroup[0],",endindex:",indexgroup[1])          
            if dist <= DTW_DISTANCE_THRESHOLD:
                true_to_true_count += 1
            else:
                true_to_false_count += 1 
    for key,value in falseDict.items():
        pricederivatList = pricederivatDict[key]
        for indexgroup in value:
            mainpriceseq = pricederivatList[indexgroup[0]:indexgroup[1]+1]
            dist, offset = subsequencedtw.subDtw(queryseq, mainpriceseq)
#             dist, offset = querySubDtw(queryCode,queryStartIndex,queryEndIndex,key,indexgroup[0],indexgroup[1])
#             if dist == None:
#                 dist, offset = subsequencedtw.subDtw(queryseq, mainpriceseq)
#                 saveSubDtw(queryCode,queryStartIndex,queryEndIndex,key,indexgroup[0],indexgroup[1],dist,offset)         
#             if risefallflag == 'fall':
#                 print("false dist:",dist,"code:",key,",startindex:",indexgroup[0],",endindex:",indexgroup[1])
            if dist <= DTW_DISTANCE_THRESHOLD:
                false_to_true_count += 1
            else:
                false_to_false_count += 1
    totalcount=true_to_true_count+true_to_false_count+false_to_true_count+false_to_false_count
    ft=(true_to_true_count+false_to_true_count)/totalcount
    ff=(true_to_false_count+false_to_false_count)/totalcount
    pta=true_to_true_count/(true_to_true_count+false_to_true_count)
    ptb=false_to_true_count/(true_to_true_count+false_to_true_count)
    i1=0
    if pta != 0 and ptb != 0:
        i1= -pta*math.log(pta,2)-ptb*math.log(ptb,2)
    if ff == 0:
        return ft*i1
    pfa=true_to_false_count/(true_to_false_count+false_to_false_count)
    pfb=false_to_false_count/(true_to_false_count+false_to_false_count)
    i2=0
    if pfa != 0 and pfb != 0:
        i2= -pfa*math.log(pfa,2)-pfb*math.log(pfb,2)   
    return ft*i1+ff*i2

sb_set = db.sb_set
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
priceDict={}
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
    pricederivatelist = []
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricederivatelist.append(j['derivative']) 
        pricelist.append(j['close'])       
    pricederivatDict[code]=pricederivatelist
    priceDict[code]=pricelist


print("del rise")  
for key,value in riseDict.items():
    pricederivatList = pricederivatDict[key]
    pricelist = priceDict[key]
    maxprice = 0
    for i in pricelist:
        if i > maxprice:
            maxprice = i
    print("del stock:",key)
    feature_group=[]
    gain_group=[]
    for indexgroup in value:
        startindex=indexgroup[0]
        endindex=indexgroup[1]
        for stocklang in range(SEQ_MIN_LEN,SEQ_MAX_LEN+1):
            if stocklang > (endindex-startindex+1):
                break
            for offset in range(0,endindex-startindex+1-stocklang+1):
                endprice = pricelist[startindex+offset+stocklang-1]
                if (maxprice-endprice)/endprice < 0.2:
                    print("stock:",key,"begin,startindex:",startindex,",endindex:",endindex,",len:",stocklang,",offset:",offset,"is to near max continue!!!")
                    continue
                print("get stock:",key,"begin,startindex:",startindex,",endindex:",endindex,",len:",stocklang,",offset:",offset)
                queryseq=pricederivatList[startindex+offset:startindex+offset+stocklang]
                print("queryseq:",queryseq)
                seqentropy=getseqentropy(queryseq,riseDict,unriseDict,pricederivatDict,key,startindex+offset,startindex+offset+stocklang-1,'rise')
                gain=riseGroupEntropy-seqentropy
                print("seqentropy:",seqentropy,"gain:",gain)
                if gain >= GAIN_THRESHOLD:
                    print("get stock:",key,"begin,startindex:",startindex+offset,",endindex:",startindex+offset+stocklang-1)
                    feature_group.append([startindex+offset,startindex+offset+stocklang-1])
                    gain_group.append(gain)
    if len(feature_group):
        rise_feature_set.insert_one({"code":key,"featuregroup":feature_group,"gaingroup":gain_group})    
        
                    
print("del fall")                     
for key,value in fallDict.items():
    pricederivatList = pricederivatDict[key]
    pricelist = priceDict[key]
    minprice = float("inf")
    for i in pricelist:
        if i < minprice:
            minprice = i
    print("del stock:",key)
    feature_group=[]
    gain_group=[]
    for indexgroup in value:
        startindex=indexgroup[0]
        endindex=indexgroup[1]
        for stocklang in range(SEQ_MIN_LEN,SEQ_MAX_LEN+1):
            if stocklang > (endindex-startindex+1):
                break
            for offset in range(0,endindex-startindex+1-stocklang+1):
                endprice = pricelist[startindex+offset+stocklang-1]
                if (endprice-minprice)/endprice > 0.3:
                    print("stock:",key,"begin,startindex:",startindex,",endindex:",endindex,",len:",stocklang,",offset:",offset,"is to near min continue!!!")
                    continue
                print("get stock:",key,"begin,startindex:",startindex,",endindex:",endindex,",len:",stocklang,",offset:",offset)
                queryseq=pricederivatList[startindex+offset:startindex+offset+stocklang]
                print("queryseq:",queryseq)
                seqentropy=getseqentropy(queryseq,fallDict,unfallDict,pricederivatDict,key,startindex+offset,startindex+offset+stocklang-1,'fall')
                gain=fallGroupEntropy-seqentropy
                print("seqentropy:",seqentropy,"gain:",gain)
                if gain >= GAIN_THRESHOLD:
                    print("get stock:",key,"success,startindex:",startindex+offset,",endindex:",startindex+offset+stocklang-1)
                    feature_group.append([startindex+offset,startindex+offset+stocklang-1])
                    gain_group.append(gain)
    if len(feature_group):
        fall_feature_set.insert_one({"code":key,"featuregroup":feature_group,"gaingroup":gain_group})    
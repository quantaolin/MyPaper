'''
Created on 2018-07-07 09:17

@author: quantaolin
'''
from pymongo import MongoClient
import math

GAIN_THRESHOLD=0.5
DTW_DISTANCE_THRESHOLD=10

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

    
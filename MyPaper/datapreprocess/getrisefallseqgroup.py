'''
Created on  2018-07-23 17:55:02

@author: quantaolin
'''
from pymongo import MongoClient

around_minpoint_rise=0.1
around_maxpoint_fall=0.1
horizontal_before_rise_min_len=10
horizontal_before_fall_max_len=5


def getrisegroup(pricelist,key_point_indexs,key_point_riseandfall_flags):
    rise_index_group=[]
    unrise_index_group=[]
    for i in range(len(key_point_indexs)):
        index = key_point_indexs[i]
        flag = key_point_riseandfall_flags[i]
        nextindex = len(pricelist)-1
        if i != len(key_point_indexs)-1: 
            nextindex = key_point_indexs[i+1]
        if flag < 0:
            unrise_index_group.append([index,nextindex]) 
        elif flag > 0:
            start_index=index-1
            end_index=index+1
            while True:
                if start_index <= 0:
                    start_index = 0
                    break
                if pricelist[start_index]-pricelist[index]/pricelist[index] > around_minpoint_rise:
                    start_index = start_index+1
                    break
                start_index = start_index-1
            while True:
                if end_index >= len(pricelist)-1:
                    end_index = len(pricelist)-1
                    break
                if pricelist[end_index]-pricelist[index]/pricelist[index] > around_minpoint_rise:
                    end_index = end_index-1
                    break
                end_index = end_index+1
            if end_index - start_index < horizontal_before_rise_min_len:
                unrise_index_group.append([index,nextindex])
            else:
                rise_index_group.append([start_index,end_index])
                last_unindex_group=unrise_index_group[-1]
                last_unindex_group[-1]=start_index
                if end_index < nextindex:
                    unrise_index_group.append([end_index,nextindex])              
    return rise_index_group,unrise_index_group

def getfallgroup(pricelist,key_point_indexs,key_point_riseandfall_flags):
    fall_index_group=[]
    unfall_index_group=[]
    for i in range(len(key_point_indexs)):
        index = key_point_indexs[i]
        flag = key_point_riseandfall_flags[i]
        nextindex = len(pricelist)-1
        if i != len(key_point_indexs)-1: 
            nextindex = key_point_indexs[i+1]
        if flag > 0:
            unfall_index_group.append([index,nextindex])
        elif flag < 0:
            start_index=index-1
            end_index=index+1
            while True:
                if start_index <= 0:
                    start_index = 0
                    break
                if pricelist[index]-pricelist[start_index]/pricelist[index] > around_maxpoint_fall:
                    start_index = start_index+1
                    break
                start_index = start_index-1
            while True:
                if end_index >= len(pricelist)-1:
                    end_index = len(pricelist)-1
                    break
                if pricelist[index]-pricelist[end_index]/pricelist[index] > around_maxpoint_fall:
                    end_index = end_index-1
                    break
                end_index = end_index+1
            if end_index - start_index < horizontal_before_fall_max_len:
                unfall_index_group.append([index,nextindex])
            else:
                fall_index_group.append([start_index,end_index])
                last_unindex_group=unfall_index_group[-1]
                last_unindex_group[-1]=start_index
                if end_index < nextindex:
                    unfall_index_group.append([end_index,nextindex])              
    return fall_index_group,unfall_index_group


conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.sb_set
seq_set = db.seq_set
rise_set = db.rise_set
unrise_set = db.unrise_set
fall_set = db.fall_set
unfall_set = db.unfall_set

for i in sb_set.find():
    code = i['code']
    
    collist = db.collection_names()
    if code not in collist:
        print("code:",code," is not have continue")
        continue
    
    tmp_set = db[code]
    pricelist = [] 
    for j in tmp_set.find().sort("data"):
        pricelist.append(j['close'])
    
    seq = seq_set.find({ "code": code })
    key_point_indexs = seq[0]["key_point_indexs"]
    key_point_riseandfall_flags = seq[0]["key_point_riseandfall_flags"]
    
    rise_index_group,unrise_index_group = getrisegroup(pricelist,key_point_indexs,key_point_riseandfall_flags)
    rise_set.insert({"code":code,"index_group":rise_index_group})
    unrise_set.insert({"code":code,"index_group":unrise_index_group})
    
    fall_index_group,unfall_index_group = getfallgroup(pricelist,key_point_indexs,key_point_riseandfall_flags)
    fall_set.insert({"code":code,"index_group":fall_index_group})
    unfall_set.insert({"code":code,"index_group":unfall_index_group})
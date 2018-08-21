'''
Created on  2018-07-23 17:55:02

@author: quantaolin
'''
from pymongo import MongoClient

before_minpoint_rise=0.1
after_minpoint_rise_max_rise=0.3
before_maxpoint_fall=0.1
after_maxpoint_fall=0.3
horizontal_before_rise_min_len=10
horizontal_before_fall_max_len=5


def getrisegroup(pricelist,key_point_indexs,key_point_riseandfall_flags,datalist):
    rise_index_group=[]
    unrise_index_group=[]
    for i in range(len(key_point_indexs)):
        index = key_point_indexs[i]
        flag = key_point_riseandfall_flags[i]
        print("index:",index,",flag:",flag)
        nextindex = len(pricelist)-1
        if i != len(key_point_indexs)-1: 
            nextindex = key_point_indexs[i+1]
        print("nextindex:",nextindex,",value:",pricelist[index],",data:",datalist[index])
        if flag < 0:
            print("fallindex,value:",pricelist[index],",data:",datalist[index])
            unrise_index_group.append([index,nextindex]) 
        elif flag > 0:
            start_index=index-1
            end_index=index+1
            print("find startindex and endindex,value:",pricelist[index],",data:",datalist[index])
            while True:
                print("startindex:",start_index,",value:",pricelist[start_index],",date:",datalist[start_index])
                if start_index <= 0:
                    start_index = 0
                    break
                if (pricelist[start_index]-pricelist[index])/pricelist[index] > before_minpoint_rise:
                    start_index = start_index+1
                    break
                start_index = start_index-1
            while True:
                print("endindex:",end_index,",value:",pricelist[end_index],",data:",datalist[end_index])
                if end_index >= len(pricelist)-1:
                    end_index = len(pricelist)-1
                    break
                if (pricelist[nextindex]-pricelist[end_index])/pricelist[end_index] < after_minpoint_rise_max_rise:
                    end_index = end_index-1
                    break
                end_index = end_index+1
            print("startindex:",start_index,",end_index:",end_index)
            if end_index - start_index + 1 < horizontal_before_rise_min_len:
                unrise_index_group.append([index,nextindex])
            else:
                rise_index_group.append([start_index,end_index])
                if unrise_index_group:
                    last_unindex_group=unrise_index_group[-1]
                    last_unindex_group[-1]=start_index              
                if end_index < nextindex:
                    unrise_index_group.append([end_index,nextindex])              
    return rise_index_group,unrise_index_group

def getfallgroup(pricelist,key_point_indexs,key_point_riseandfall_flags,datalist):
    fall_index_group=[]
    unfall_index_group=[]
    for i in range(len(key_point_indexs)):
        index = key_point_indexs[i]
        flag = key_point_riseandfall_flags[i]
        print("index:",index,",flag:",flag)
        nextindex = len(pricelist)-1
        if i != len(key_point_indexs)-1: 
            nextindex = key_point_indexs[i+1]
        print("nextindex:",nextindex,",value:",pricelist[index],",data:",datalist[index])
        if flag > 0:
            print("riseindex,value:",pricelist[index],",data:",datalist[index])
            unfall_index_group.append([index,nextindex])
        elif flag < 0:
            start_index=index-1
            end_index=index+1
            print("find startindex and endindex,value:",pricelist[index],",data:",datalist[index])
            while True:
                print("startindex:",start_index,",value:",pricelist[start_index],",date:",datalist[start_index])
                if start_index <= 0:
                    start_index = 0
                    break
                if (pricelist[index]-pricelist[start_index])/pricelist[index] > before_maxpoint_fall:
                    start_index = start_index+1
                    break
                start_index = start_index-1
            while True:
                print("endindex:",end_index,",value:",pricelist[end_index],",data:",datalist[end_index])
                if end_index >= len(pricelist)-1:
                    end_index = len(pricelist)-1
                    break
                if (pricelist[index]-pricelist[end_index])/pricelist[index] > after_maxpoint_fall:
                    end_index = end_index-1
                    break
                end_index = end_index+1
            print("startindex:",start_index,",end_index:",end_index)
            if end_index - start_index + 1 < horizontal_before_fall_max_len:
                unfall_index_group.append([index,nextindex])
            else:
                fall_index_group.append([start_index,end_index])
                if unfall_index_group:
                    last_unindex_group=unfall_index_group[-1]
                    last_unindex_group[-1]=start_index            
                if end_index < nextindex:
                    unfall_index_group.append([end_index,nextindex])              
    return fall_index_group,unfall_index_group


conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb
sb_set = db.train_sb_set
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
    print("get stock:",code," price fall rise seq")
    tmp_set = db[code]
    pricelist = []
    datalist = []
    for j in tmp_set.find().sort("data"):
        datalist.append(j['data'])
        pricelist.append(j['close'])
    
    print("pricelist:",pricelist)
    
    seq = seq_set.find({ "code": code })
    key_point_indexs = seq[0]["key_point_indexs"]
    key_point_riseandfall_flags = seq[0]["key_point_riseandfall_flags"]
    print("key_point_indexs:",key_point_indexs)
    
    rise_index_group,unrise_index_group = getrisegroup(pricelist,key_point_indexs,key_point_riseandfall_flags,datalist)
    print("risegroup:",rise_index_group)
    print("unrisegroup:",unrise_index_group)
    rise_set.insert({"code":code,"index_group":rise_index_group})
    unrise_set.insert({"code":code,"index_group":unrise_index_group})
    
    fall_index_group,unfall_index_group = getfallgroup(pricelist,key_point_indexs,key_point_riseandfall_flags,datalist)
    print("fallgroup:",fall_index_group)
    print("unfallgroup:",unfall_index_group)
    fall_set.insert({"code":code,"index_group":fall_index_group})
    unfall_set.insert({"code":code,"index_group":unfall_index_group})
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
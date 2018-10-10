'''
Created on 2018-08-19 01:54

@author: linqt
'''

def deal(querySeq,majorSeq):
    return "dist","path"

def getCostMatrix(querySeq,majorSeq):
    costMatrix = [[0]*len(majorSeq) for i in range(len(querySeq))]
    for p in range(len(querySeq)):
        row=[]
        queryIndex = querySeq[p]
        for q in range(len(majorSeq)):
            majorIndex = majorSeq[q]
            distance = abs(queryIndex - majorIndex)
            row.append(distance)
        costMatrix.append(row)
    return costMatrix

def getDtw(costMatrix,b):
    pass
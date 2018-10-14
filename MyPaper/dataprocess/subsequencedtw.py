'''
Created on 2018-08-19 01:54

@author: linqt
'''

def deal(querySeq,majorSeq):
    xIndex = len(querySeq) - 1
    maxY = len(majorSeq) - 1
    dist = float('inf')
    path = []
    costMatrix = getCostMatrix(querySeq,majorSeq)
    print("costMatrix:",costMatrix)
    for i in range(maxY + 1):
        tmpDist,tmpPath = getDtw(costMatrix,xIndex,maxY-i)
        print("xIndex:",xIndex,",yIndex:",maxY-i,",dist:",tmpDist)
        if tmpDist < dist:
            print("this is the nearest")
            dist = tmpDist
            path = tmpPath
    print("the nearest dist is:",dist)
    return dist,path

def getCostMatrix(querySeq,majorSeq):
    costMatrix = []
    for p in range(len(querySeq)):
        row=[]
        queryIndex = querySeq[p]
        for q in range(len(majorSeq)):
            majorIndex = majorSeq[q]
            distance = round(abs(queryIndex - majorIndex)*1000,2)
            row.append(distance)
        costMatrix.append(row)
    return costMatrix

def getDtw(costMatrix,xIndex,yIndex):
    if xIndex == 0:
        return costMatrix[xIndex][yIndex],[[xIndex,yIndex]]
    elif yIndex == 0:
        nextDistance,nextPath = getDtw(costMatrix,xIndex-1,yIndex)
        return costMatrix[xIndex][yIndex]+nextDistance,[[xIndex,yIndex]].extend(nextPath)
    else :
        nextDistance,nextPath = getDtw(costMatrix,xIndex-1,yIndex)
        nextDistance2,nextPath2 = getDtw(costMatrix,xIndex-1,yIndex-1)
        if nextDistance2 < nextDistance:
            nextDistance = nextDistance2
            nextPath = nextPath2
        nextDistance3,nextPath3 = getDtw(costMatrix,xIndex,yIndex-1)
        if nextDistance3 < nextDistance:
            nextDistance = nextDistance3
            nextPath = nextPath3
        return costMatrix[xIndex][yIndex]+nextDistance,[[xIndex,yIndex]].extend(nextPath)
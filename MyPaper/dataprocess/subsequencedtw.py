'''
Created on 2018-08-19 01:54

@author: linqt
'''
import datetime

SEQ_MAX_LEN=20
DTW_WINDOW_T=5

def deal(querySeq,majorSeq):
    starttime = datetime.datetime.now()
    xIndex = len(querySeq) - 1
    maxY = len(majorSeq) - 1
    dist = float('inf')
    path = []
    costMatrix = getCostMatrix(querySeq,majorSeq)
#     print("costMatrix:",costMatrix)
    minY = xIndex
    if minY > maxY:
        minY = maxY
    for i in range(minY,maxY + 1):
        yIndexStart = 0
        if i > (SEQ_MAX_LEN-1):
            yIndexStart = i-SEQ_MAX_LEN+1
        tmpDist,tmpPath = getDtw(costMatrix,xIndex,i,yIndexStart)
#         print("xIndex:",xIndex,",yIndex:",i,",dist:",tmpDist)
        if tmpDist == 0:
#             print("this is the zore")
            dist = tmpDist
            path = tmpPath
            break
        if tmpDist < dist:
#             print("this is the nearest")
            dist = tmpDist
            path = tmpPath
    endtime = datetime.datetime.now()
    print("the nearest dist is:",dist,",usetime:",(endtime - starttime).seconds)
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

def getDtw(costMatrix,xIndex,yIndex,minY):
    if abs(yIndex-xIndex) > DTW_WINDOW_T:
        return float("inf"),[[xIndex,yIndex]]
    if xIndex == 0 and yIndex > minY:
        nextDistance,nextPath = getDtw(costMatrix,xIndex,yIndex-1,minY)
        path=[[xIndex,yIndex]]
        path.extend(nextPath)
        return costMatrix[xIndex][yIndex]+nextDistance,path
    elif xIndex > 0 and yIndex == minY:
        nextDistance,nextPath = getDtw(costMatrix,xIndex-1,yIndex,minY)
        path=[[xIndex,yIndex]]
        path.extend(nextPath)
        return costMatrix[xIndex][yIndex]+nextDistance,path
    elif xIndex == 0 and yIndex == minY:
        return costMatrix[xIndex][yIndex],[[xIndex,yIndex]]
    else :
        nextDistance,nextPath = getDtw(costMatrix,xIndex-1,yIndex,minY)
        nextDistance2,nextPath2 = getDtw(costMatrix,xIndex-1,yIndex-1,minY)
        if nextDistance2 < nextDistance:
            nextDistance = nextDistance2
            nextPath = nextPath2
        nextDistance3,nextPath3 = getDtw(costMatrix,xIndex,yIndex-1,minY)
        if nextDistance3 < nextDistance:
            nextDistance = nextDistance3
            nextPath = nextPath3
        path=[[xIndex,yIndex]]
        path.extend(nextPath)
        return costMatrix[xIndex][yIndex]+nextDistance,path
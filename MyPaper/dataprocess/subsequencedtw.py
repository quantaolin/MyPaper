'''
Created on 2018-08-19 01:54

@author: linqt
'''
import datetime    

def subDtw(querySeq,majorSeq):
    distanceMatrix = getDistanceMatrix(querySeq,majorSeq)
    lenx = len(querySeq)
    leny = len(majorSeq)
    costMatrix = getCostMatrix(distanceMatrix,lenx,leny)
    endCost = costMatrix[lenx-1]
    minDistance = float("inf")
    offset = 0
    for i in range(1,leny):
        if endCost[i] < minDistance:
            minDistance = endCost[i]
            offset = i-1
    return minDistance,offset

def getDistanceMatrix(querySeq,majorSeq):
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

def min(a,b,c):
    min = a
    if b < min:
        min = b
    if c < min:
        min = c
    return min

def getCostMatrix(distanceMatrix,lenx,leny):
    costMatrix=[[float("inf") for i in range(leny+1)] for i in range(lenx+1)]
    for i in range(1,leny+1):
        costMatrix[0][i]=0
    for i in range(1,lenx+1):
        for j in range(1,leny+1):
            if(i == 1) :
                costMatrix[i][j]=distanceMatrix[i-1][j-1]
            costMatrix[i][j]=distanceMatrix[i-1][j-1]+min(costMatrix[i-1][j],costMatrix[i][j-1],costMatrix[i-1][j-1])
    return costMatrix

def subByEd(querySeq,majorSeq):
    xIndex = len(querySeq) - 1
    maxY = len(majorSeq) - 1
    dist = float('inf')
    distanceMatrix = getDistanceMatrix(querySeq,majorSeq)
    minY = xIndex
    if minY > maxY:
        minY = maxY
        return float('inf')
    for i in range(minY,maxY + 1):
        yIndexStart = 0
        if i > (len(querySeq)-1):
            yIndexStart = i-len(querySeq)+1
        tmpDist = getEDistance(distanceMatrix,xIndex,i,yIndexStart)
        if tmpDist == 0:
            dist = tmpDist
            break
        if tmpDist < dist:
            dist = tmpDist
    return dist

def getEDistance(distanceMatrix,xIndex,yIndex,minY):
    if xIndex == 0 and yIndex == minY:
        return distanceMatrix[xIndex][yIndex]
    else :
        nextDistance = getEDistance(distanceMatrix,xIndex-1,yIndex-1,minY)
        return distanceMatrix[xIndex][yIndex]+nextDistance
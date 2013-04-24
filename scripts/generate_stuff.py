#!/usr/bin/python

import argparse
import random

countMap = {}

def buildCountMap(fileHandle):
    with open(fileHandle) as f:
        for line in f:
            parts = line.split(';')
            countMap[parts[0]] = parts[1:]


def getNextWord(listOfStuff):
    bigTuples = []
    allCounts = 0
    newTuples = []
    for x in listOfStuff:
        parts = x.split(',')
        bigTuples.append((parts[0], parts[1]))
        allCounts += int(parts[1])
    for x in bigTuples:
        newTuple = (x[0], float(x[1])/float(allCounts))
        newTuples.append(newTuple)
    valuething = random.random()
    newSum = 0
    for x in newTuples:
        newSum += x[1]
        if valuething < newSum:





def generateWords(numWords):
    count = 0
    currentStr = ""
    while count <= numWords:
        if currentStr in countMap:
            getNextWord(countMap[currentStr])


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
            return x[0]
    print "no match?"
    

def generateWords(numWords):
    count = 0
    currentStr = ""
    while count <= numWords:
        if currentStr in countMap:
            currentStr += getNextWord(countMap[currentStr])
            count += 1
            continue
    return currentStr

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputf', nargs='?', required=True)
    args = parser.parse_args()

    buildCountMap(args.inputf)
    print generateWords(10)

if __name__=="__main__":
    main()

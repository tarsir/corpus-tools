#!/usr/bin/python

import argparse
import random

countMap = {}
phoneMap = {}
phoneStats = {}
fillers = ["ooh", "ahh", "yeah", "girl", "uh"]

def averagePhonesPerLetter():
    phoneStats[1] = [1]
    for word, phones in phoneMap.iteritems():
        endofword = len(word)
        if endofword not in phoneStats:
            phoneStats[endofword] = []
        phoneStats[endofword].append(len(phones))
    for wordLen, phonecount in phoneStats.iteritems():
        phoneStats[wordLen] = reduce(lambda x,y: x + y, phonecount) / len(phonecount)
        # print "Defaulting {0} letter words to {1} syllables".format(wordLen, phoneStats[wordLen])


def buildPhoneMap(fileName):
    with open(fileName) as f:
        for line in f:
            parts = line.split(':')
            parts[1] = parts[1].split(',')
            phoneMap[parts[0]] = parts[1]

def buildCountMap(fileHandle):
    with open(fileHandle) as f:
        for line in f:
            parts = line.split(';')
            countMap[parts[0]] = parts[1:]

def getNextWord(listOfStuff):
    """
    """
    bigTuples = []
    allCounts = 0
    newTuples = []
    for x in listOfStuff:
        x = x.strip()
        comindex = x.rfind(',')
        parts = [x[:comindex], x[comindex+1:]]
        if len(parts) <= 1 or ''.join(parts).strip() == '':
            break
        try:
            allCounts += int(parts[1])
            bigTuples.append((parts[0], parts[1]))
        except ValueError:
            pass
            # print parts
    for x in bigTuples:
        newTuple = (x[0], float(x[1])/float(allCounts))
        newTuples.append(newTuple)
    valuething = random.random()
    newSum = 0
    for x in newTuples:
        newSum += x[1]
        if valuething < newSum:
            return x[0]
    # print "no match?"
    return ""

def generateWords(numWords):
    count = 0
    currentStr = []
    window = []
    while count <= numWords:
        window = currentStr
        windowStart = 0
        while ' '.join(window) not in countMap:
            windowStart += 1
            window = currentStr[windowStart:]
        currentStr.append(getNextWord(countMap[' '.join(window)]))
        count += 1
    return ' '.join(currentStr)

def generateWordsSyllableCount(numsyllables):
    curSylls = 0
    currentStr = []
    window = []
    while curSylls <= numsyllables:
        windowStart = 0
        while ' '.join(window) not in countMap:
            windowStart += 1
            window = currentStr[windowStart:]
        joinedStr = ' '.join(window)
        if joinedStr in countMap:
            candidates = []
            for x in countMap[joinedStr]:
                parts = x.split(',')
                newSylls = 0
                if parts[0] in phoneMap:
                    newSylls = len(phoneMap[parts[0]])
                else:
                    try:
                        newSylls = phoneStats[len(parts[0])]
                    except KeyError:
                        newSylls = len(parts[0])/2+2
                if curSylls+newSylls > numsyllables+5:
                    continue
                candidates.append(x)
            if len(candidates) == 0 or curSylls - numsyllables in range(-4, 4):
                candidates.append((random.choice(fillers), 1))
            currentStr.append(getNextWord(candidates))
            curSylls += newSylls
    return currentStr



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-cm', '--countmap', nargs='?', required=True)
    parser.add_argument('-pm', '--phrasemap', nargs='?', required=True)
    parser.add_argument('-n', '--count', nargs='?', default=5)
    args = parser.parse_args()

    buildCountMap(args.countmap)
    buildPhoneMap(args.phrasemap)
    averagePhonesPerLetter()
    iterations = int(args.count)
    for i in range(0, iterations):
        print generateWords(20)
    # print generateWordsSyllableCount(40)

if __name__=="__main__":
    main()

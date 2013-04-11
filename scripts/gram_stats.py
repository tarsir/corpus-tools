#!/usr/bin/python

from splitBySeps import divideBySeps as splitter, combineSeps as combiner
import argparse
import string

EMPTY_PIECE="_"

class Ngram:
    gram = []
    count = 0

def parseGram(gramStr):
    radGram = Ngram()
    cutoff = string.rfind(gramStr, ':')
    radGram.count = int(gramStr[cutoff+1:])
    print radGram.count
    radGram.gram = combiner(splitter(gramStr[:cutoff]))
    print gramStr
    print radGram.gram
    return radGram

parseGram("'hello, this is a dog':5")

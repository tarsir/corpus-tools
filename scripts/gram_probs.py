#!/usr/bin/python
'''
    This file prefers a sorted input that has had
    n-grams of count 1 removed for the purposes of
    efficiency and data set size.
'''

import argparse
from analyze_text import Ngram

def addIntoCountMap(count_map, ngram):
    '''
    count_map: a {str:[(str,int)]} map of (n-1)-grams
        to a tuple of the n-th word and the frequency of the
        given n-th word
    ngram: an Ngram object to be added into the map
    '''
    ngram_key = ' '.join(ngram.gram[:len(ngram.gram)-1])
    ngram_tuple = (ngram.gram[-1], ngram.count)
    if ngram_key in count_map:
        count_map[ngram_key].append(ngram_tuple)
    else:
        count_map[ngram_key] = [ngram_tuple]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputf', nargs='+', required=True)
    args = parser.parse_args()

    ourCounts = {}

    for inp_file in args.inputf:
        with open(inp_file) as f:
            for line in f:
                pivot_point = line.rfind(':')
                gramText = line[:pivot_point]
                gramText = gramText.strip('\'')
                gramCount = line[pivot_point+1:]
                gramCount = gramCount.strip()
                gramText = gramText.split()
                ourGram = Ngram(gramText, gramCount)
                if len(gramText) > 0:
                    addIntoCountMap(ourCounts, ourGram)
    for key, val in ourCounts.items():
        valString = ''
        for x in val:
            valString += x[0] + ',' + x[1] + ';'
        print '{:<35}\t;{}'.format(key.strip('\''), valString)

if __name__=="__main__":
    main()

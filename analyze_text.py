#!/usr/bin/python

import argparse
import re
import operator
import string
import codecs

# Globals!
# Pretty self-explanatory, I think.  Might make a more detailed doc
# file at some point, buuut too lazy.

separators = [',', ' ', '.', '?', '!', ';', '\n']
final_sep = ['.', '?', '!', '\n', ';']
EMPTY_PIECE = "1_EMPTY"     # this is for empty spots, eg. <E, E, "Hello"> for
                            # n-grams at the beginning of a phrase.

# Class defs
# Ngram: Abstraction of the mathematical n-gram
# ex: gramEx = Ngram()
#    gramEx.gram = [EMPTY_PIECE, "What", "are", "you", "doing?"]
#    gramEx.count = 2
#    here n = 5
#    I'm not actually sure why I have this class def but whatever

class Ngram:
    gram = []
    count = 0

# Node: I don't know what this is for.

class Node:
    def __init__(self):
        pass

# Function defs
# charCounts: Returns a count of every character in the source file
# Not terribly useful at the moment since it doesn't do anything
# sequentially...

def charCounts(in_file):
    charCountMap = {}
    with codecs.open(in_file, encoding='utf-8') as f:
        for line in f:
            for x in range(0, len(line)):
                if line[x] == '\n':
                    pass
                elif line[x] in charCountMap: #increment count of line[x]
                    charCountMap[unicode(line[x])] = charCountMap[unicode(line[x])] + 1
                else:  # special case where line[x] isn't already in the map
                    charCountMap[unicode(line[x])] = 1

    sorted_map = sorted(charCountMap.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_map

# charCountsGram: Returns a map of character-level n-grams in the source
# file.  Doesn't actually work at the moment for a variety of reasons.

def charCountsGram(in_file, nval = 3):
    # I don't know what these variables do oh god why
    gramCountMap = {}
    ngram_list = []
    cur_gram = Ngram()
    with codecs.open(in_file, encoding='utf-8') as f:
        for line in f:
            for x in range(0, len(line)):
                if len(cur_gram.gram) >= nval - 1:
                    cur_gram.gram.pop[0]
                if ngram_list.count(cur_gram.gram) :
                    gramCountMap[cur_gram] += 1
                else:
                    gramCountMap[cur_gram] = 1
                if line[x] == '\n':
                    cur_gram = []
                else:
                    cur_gram.append(line[x])

    sorted_map = sorted(gramCountMap.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_map

# wordCounts: Counts the words in the file.  Like charCounts, isn't
# sequential, so not terribly useful...

def wordCounts(in_file):
    wordCountMap = {}
    words = []
    with open(in_file) as f:
        for line in f:
            a_word = ""
            vals = range(0, len(line))
            for c_index in vals:
                char = line[c_index]
                if separators.count(char) > 0:
                    words.append(a_word)
                    if a_word in wordCountMap:
                        wordCountMap[a_word] = wordCountMap[a_word] + 1
                    else:
                         wordCountMap[a_word] = 1
                    words.append(char)
                    a_word = ""
                else:
                    a_word += char
    sorted_map = sorted(wordCountMap.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_map

# phraseCounts: Returns a list of word-level n-grams (where n = max_words), along with
# their counts in in_file.  Closer to what we want, and also a giant mess of spaghetti.
# There is, hidden in here, an algorithm, but it's easier to sketch it on a piece of
# paper and scan it than it is to comment this behemoth.

def phraseCounts(in_file, max_words = 3):
    phraseCountMap = {}
    phrases = []
    first_sep_index = 0
    second_sep_index = 0
    cur_word = 0
    sentence_end_index = 0
    first_sep_c_index = 0
    with open(in_file) as f:
        for line in f:
            phrase = ""
            sentence_end_index = 0
            vals = range(0, len(line))
            for c_index in vals:
                char = line[c_index]
                phrase += char
                is_seps = True
                if separators.count(char) > 0:
                    if c_index+1 < len(line) and separators.count(line[c_index+1]):
                        pass
                    else:
                        for x in phrase:
                            if separators.count(x) == 0:
                                is_seps = False
                        if final_sep.count(char) > 0 and not is_seps:
                            if not is_seps:
                                #print '\'{0}\' NOT SEPS'.format(phrase.rstrip('\n'))
                                phrases.append(phrase)
                                sentence_end_index = c_index + 1
                                phrase = ""
                                cur_word = 0
                        elif not is_seps:
                            #print '\'{0}\''.format(phrase)
                            cur_word += 1
                            if cur_word == 1:
                                first_sep_index = c_index - (sentence_end_index)
                                #print 'Set first_sep_index to: {0}'.format(first_sep_index)
                                #print 'c_index={0}\nsentence_end_index={1}'.format(c_index, sentence_end_index)
                                first_sep_c_index = first_sep_index
                            elif cur_word == 2:
                                second_sep_index = c_index - (sentence_end_index )
                                #print 'Set second_sep_index to: {0}'.format(second_sep_index)
                                #print 'c_index={0}\nsentence_end_index={1}'.format(c_index, sentence_end_index)
                            elif cur_word == max_words:
                                cur_word -= 1
                                phrases.append(phrase)
                                #print 'Cutoffs ONE: {0} and {1}'.format(first_sep_index, second_sep_index)
                                #print 'Phrases ONE: \n\t\'{0}\'\n\t\'{1}\''.format(phrase[first_sep_index:], phrase[second_sep_index:])
                                #print '\'{0}\''.format(phrase)
                                #print '\'{0}\''.format(phrase[:-1])
                                temp = unicode(phrase[:len(phrase) -1 ].strip())
                                if temp in phraseCountMap:
                                    phraseCountMap[temp] += 1
                                else:
                                    phraseCountMap[temp] = 1
                                phrase = phrase[first_sep_index:]
                                #print '\'{0}\''.format(phrase)
                                #print 'RELEVANT VARS:\nc_index={0}\nfirst_sep_index={1}\nsecond_sep_index={2}\nsentence_end_index={3}'.format(c_index, first_sep_index, second_sep_index, sentence_end_index)
                                first_sep_index, second_sep_index = second_sep_index - first_sep_index, c_index - first_sep_c_index + 1 - sentence_end_index
                                #print 'INDICES: {0}, {1}, {2}'.format(first_sep_index, second_sep_index, first_sep_c_index)
                                first_sep_c_index += first_sep_index
#                            second_sep_index = c_index + 1
                                #print 'Cutoffs TWO: {0} and {1}'.format(first_sep_index, second_sep_index)
                                #print 'Phrases TWO: {0}\n{1}'.format(phrase[first_sep_index:], phrase[second_sep_index:])
                            if final_sep.count(char) > 0:
                                phrases.append(phrase)
                            elif is_seps:
                                phrase = ""
                                is_seps = True
    sorted_map = sorted(phraseCountMap.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_map

# the ubiquitous main()

def main():
    parser = argparse.ArgumentParser(description='') #TODO: add desc
    parser.add_argument('-i', '--inputF', nargs='+', required=True, help='The source files to be analyzed')
    parser.add_argument('-m', '--mode', nargs='?', default='p', help='The mode by which to analyze the input files')
    parser.add_argument('-g', '--grams', nargs='?', default=True, help='If true, will construct N-grams')
    args = parser.parse_args()

    asdf = ()
#    wordCounts(args.inputF)
    for x in string.whitespace:
        separators.append(x)

    for inp_file in args.inputF:
        if args.mode == 'p' or args.mode == 'P':
            asdf = phraseCounts(inp_file)
        elif args.mode == 'w' or args.mode == 'W':
            asdf = wordCounts(inp_file)
        elif args.mode == 'c' or args.mode == 'C':
            if args.grams:
                asdf = charCountsGram(inp_file)
            else:
                asdf = charCounts(inp_file)
        print 'IT BEGINS'
        for obj in asdf:
            x = '\'{0}\':{1}'.format(obj[0].encode('utf-8'), obj[1])
            print x

if __name__ == "__main__":
    main()

#!/usr/bin/python

from split_by_seps import divideBySeps as splitter, combineSeps as combiner
import argparse
import operator
import string
import codecs

# Globals!
# Pretty self-explanatory, I think.  Might make a more detailed doc
# file at some point, buuut too lazy.

separators = [',', ' ', '.', '?', '!', ';', '\n']
final_sep = ['.', '?', '!', '\n', ';']
EMPTY_PIECE = "_"
# this is for empty spots, eg. <E, E, "Hello"> for
# n-grams at the beginning of a phrase.

# Class defs


class Ngram:
    """
    Ngram: Abstraction of the mathematical n-gram
    ex: gramEx = Ngram()
    gramEx.gram = [EMPTY_PIECE, "What", "are", "you", "doing?"]
    gramEx.count = 2
    here n = 5
    """
    def __init__(self, gram_=[], count_=0):
        self.gram = gram_
        self.count = count_

    @property
    def gram(self):
        return self.gram

    @property
    def count(self):
        return self.count

    def __str__(self):
        return ' '.join(self.gram)

# Function defs


def charCounts(in_file):
    """
    charCounts: Returns a count of every character in the source file
    Not terribly useful at the moment since it doesn't do anything
    sequentially...
    """
    charCountMap = {}
    with codecs.open(in_file, encoding='utf-8') as f:
        for line in f:
            for x in range(0, len(line)):
                if line[x] == '\n':
                    pass
                elif line[x] in charCountMap:  #increment count of line[x]
                    charCountMap[unicode(line[x])] = charCountMap[unicode(line[x])] + 1
                else:  # special case where line[x] isn't already in the map
                    charCountMap[unicode(line[x])] = 1

    sorted_map = sorted(charCountMap.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_map

# charCountsGram: Returns a map of character-level n-grams in the source
# file.  Doesn't actually work at the moment for a variety of reasons.

def charCountsGram(in_file, nval=3):
    ngram = ""
    ngram_list_pre = []
    ngram_list_final = []
    cur_gram = Ngram()
    with codecs.open(in_file, encoding='utf-8') as f:
        for line in f:
            for x in range(0, len(line)):
                if line[x] == '\n':
                    ngram = ""
                else:
                    ngram += line[x]
                if len(ngram) > nval:
                    ngram = ngram[1:]
                    ngram_list_pre.append(ngram)
    while len(ngram_list_pre) > 0:
        grams = ngram_list_pre[0]
        cur_gram.gram = grams
        while len(cur_gram.gram) < nval and len(cur_gram.gram) > 0:
            cur_gram.gram = EMPTY_PIECE + cur_gram.gram
        if len(cur_gram.gram) != 0:
            cur_gram.count = ngram_list_pre.count(grams)
            ngram_list_final.append(cur_gram)
        ngram_list_pre[:] = (value for value in ngram_list_pre if value != grams)
        cur_gram = Ngram()

    sorted_list = sorted(ngram_list_final, key=operator.attrgetter('count'))
    return sorted_list


def wordCounts(in_file):
    """
    wordCounts: Counts the words in the file.  Like charCounts, isn't
    sequential, so not terribly useful...
    """
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
                    sorted_map = sorted(
                        wordCountMap.iteritems(),
                        key=operator.itemgetter(1),
                        reverse=True
                    )
                    return sorted_map


def betterPhraseCounts(in_file, max_words = 3):
    """
    betterPhraseCounts: I think this makes word-level n-grams, but it's a lot
    simpler code-wise than phraseCounts, which is now deleted.  Excellent!
    """
    phraseCountMap = {}
    this_gram = ""
    with open(in_file) as f:
        for line in f:
            parts = combiner(splitter(line))
            end_pos = 2 * max_words - 1
            begin_pos = 0
            while begin_pos < len(parts):
                try:
                    this_gram = unicode("".join(parts[begin_pos:end_pos]))
                except UnicodeDecodeError:
                    pass
                end_pos += 2
                begin_pos += 2
                if this_gram in phraseCountMap:
                    phraseCountMap[this_gram] += 1
                else:
                    phraseCountMap[this_gram] = 1

    sorted_map = sorted(phraseCountMap.iteritems(), key=operator.itemgetter(1), reverse=True)
    realGramList = []
    for gram_, count_ in sorted_map:
        newGram = Ngram(gram_.strip(), count_)
        realGramList.append(newGram)
    return realGramList


def sumCounts(inp_list):
    """
    sumCounts: Return a map(int, int) with the number of distinct
    n-grams with each count.  Will be useful for the probability
    later, but would just like to gather stats for funsies at the
    moment.
    """
    countMap = {}
    for gram in inp_list:
        if gram.count in countMap:
            countMap[gram.count] += 1
        else:
            countMap[gram.count] = 1
            return countMap

# the ubiquitous main()


def main():
    parser = argparse.ArgumentParser(description='') #TODO: add desc
    parser.add_argument('-i', '--inputF', nargs='+', required=True, help='The source files to be analyzed')
    parser.add_argument('-m', '--mode', nargs='?', default='p', help='The mode by which to analyze the input files(eg. pt|w|c)')
    parser.add_argument('-g', '--grams', nargs='?', default=-1, help='If greater than 1, will construct N-grams of length given')
    parser.add_argument('-c', '--count', nargs='?', const=False, help='If specified, will also output counts of n-gram quantities')
    args = parser.parse_args()

    args.count = bool(args.count)
    args.grams = int(args.grams)
    args.mode = args.mode.lower()

    asdf = ()
    for x in string.whitespace:
        separators.append(x)

    for inp_file in args.inputF:
        if args.mode in ['pt', 'p']:
            asdf = betterPhraseCounts(inp_file, args.grams)
        elif args.mode == 'w':
            asdf = wordCounts(inp_file)
        elif args.mode == 'c':
            if args.grams > 1:
                asdf = charCountsGram(inp_file, args.grams)
            else:
                asdf = charCounts(inp_file)
        for obj in asdf:
            if (args.grams > 1 or args.grams == -1):
                x = '\'{0}\':{1}'.format(''.join(obj.gram).encode('utf-8'), obj.count)
            else:
                x = '\'{0}\':{1}'.format(obj.gram.encode('utf-8'), obj.count)
            print x
        if args.count and (args.grams > 1 or args.grams == -1):
            countDict = sumCounts(asdf)
            for count, countSum in countDict.items():
                print '{0}\t{1}'.format(count, countSum)

if __name__ == "__main__":
    main()

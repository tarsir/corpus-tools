from nltk import tokenize
from string import punctuation
import sys

fname = sys.argv[1] 

fin = open(fname)
fout= open("tokenized" + fname, 'w')
tokenizer = tokenize.WhitespaceTokenizer()

for line in fin.readlines():
    if len(line) == 0:
        continue
    if line == '[chorus]\n':
        fout.write('\n' + line)
        continue
    line = tokenizer.tokenize(line)
    for i in range(len(line)):
        line[i] = line[i].lower()
        #remove beginning of line punctuation
        if line[i][0] in punctuation:
            line[i] = line[i][1:] 
        #remove end of line punctuation. loop for multiple symbols
        #somtimes there can be some bad punctuation
        while len(line[i]) > 0 and line[i][-1] in punctuation:
            line[i] = line[i][:-1]
    fout.write(' '.join(line) + '\n')

fout.close()
fin.close()

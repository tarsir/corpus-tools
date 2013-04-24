class WordDictionary:
    #build the dictionary
    def __init__(self, dict_path):
        f = open(dict_path, 'rU')
        self.wordDict = {}
        f = f.read()

        for line in f.splitlines():
            word = line.split(':')[0]
            rhymes = line.split(':')[1].split(',')
            self.wordDict[word] = rhymes
    
    #returns a list of words that rhyme. Empty list if not.
    def rhymes(self, word):
        retval = []
        if word in self.wordDict:
            retval = self.wordDict[word]
        return retval



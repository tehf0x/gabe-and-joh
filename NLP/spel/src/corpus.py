"""
Corpus based candidate matching and scoring

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
"""

import nltk

class FreqDist(nltk.FreqDist):
    """ Frequency distribution with some additional functionality """
    
    def load(self, file):
        """ Load frequency counts from file """
        self.loads(file.read())
    
    def loads(self, s):
        for line in s.split("\n"):
            if not line:
                continue
            word, count = line.split()
            self[word] = int(count)
    
    def dumps(self):
        s = ""
        for word, count in self.items():
            s += "%s\t%d\n" % (word, count)
            
        return s
    
    def dump(self, file):
        """ Save frequency counts from file """
        file.write(self.dumps())
    
    def known(self, word_list):
        """ Return a subset of word_list where each element is known """
        return set(w for w in word_list if self.has_key(w))
    
    def freq_cmp(self, w1, w2):
        f1 = self[w1]
        f2 = self[w2]
        if f1 < f2:
            return -1
        elif f1 == f2:
            return 0
        else: # f1 < f2
            return 1
    
    def sort_words(self, words, reverse=True):
        """ Sort list of words by frequency in the corpus """
        return sorted(words, cmp=self.freq_cmp, reverse=reverse)

'''
Corpus based candidate matching and scoring

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
'''

import pickle

import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import brown

sents = brown.sents()
words = brown.words()

def load(filename='corpus.pickle'):
    """ Attempt to load corpus data from pickle """
    try:
        fh = open(filename, 'r')
        #print 'Loading corpus from "%s"...' % (filename) 
        return pickle.load(fh)
        
    except IOError:
        # File not found, generate
        #print 'Generating corpus to "%s"... This can take some time...' % (filename)
        
        # Lowercase the first words in sentences
        '''sents = brown.sents()
        
        for i,s in enumerate(sents):
            sents[i][0] = sents[i][0].lower()
            words.extend(sents[i])
        '''
        words = [w.lower() for w in brown.words()]
        freq = FreqDist(words)
        
        pickle.dump(freq, open(filename, 'w'))
        
        return freq

# Load frequency distribution
freq = load()



def known(word_list):
    return set(w for w in word_list if freq.has_key(w))

def freq_cmp(w1, w2):
    f1 = freq[w1]
    f2 = freq[w2]
    if f1 < f2:
        return 1
    elif f1 == f2:
        return 0
    else: # f1 < f2
        return -1

def freq_sort(words):
    """ Sort list of words by frequency in the corpus """
    return sorted(words, freq_cmp)
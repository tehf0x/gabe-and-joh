'''
Corpus based candidate matching and scoring

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
'''

from nltk import FreqDist
from nltk.corpus import brown

""" Lowercased brown corpus """
words = [w.lower() for w in brown.words()]

""" Frequency distribution of words """
freq = FreqDist(words)

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
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


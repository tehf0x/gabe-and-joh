#!/usr/bin/env python
"""
Count word bigrams in corpus and output to stdout

@author: Johannes H. Jensen <joh@pseudoberries.com>
"""

if __name__ == '__main__':
    from nltk import bigrams
    from nltk.corpus import brown
    from corpus import FreqDist
    
    bs = bigrams(word.lower() for word in brown.words() if word.isalpha())
    fdist = FreqDist(bs)
    print fdist.dumps()
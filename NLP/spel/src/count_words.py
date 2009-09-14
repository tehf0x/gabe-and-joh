#!/usr/bin/env python
"""
Count words in corpus and output to stdout

@author: Johannes H. Jensen <joh@pseudoberries.com>
"""

if __name__ == '__main__':
    from nltk.corpus import brown, reuters
    from corpus import FreqDist
    
    fdist = FreqDist(word.lower() for word in brown.words() + reuters.words() if word.isalpha())
    print fdist.dumps()
#!/usr/bin/env python
"""
Count word bigrams in corpus 

@author: Johannes H. Jensen <joh@pseudoberries.com>
"""

'''
Created on 6 Nov 2009

@author: joh
'''

import os
import sys
import cPickle as pickle

from itertools import chain

#from nltk import trigrams, word_tokenize, sent_tokenize, FreqDist
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader
from nltk.util import ingrams

n = 3

train_path = 'data/task1_train'

print 'Loading categorized corpus in', train_path, '...'

cr = CategorizedPlaintextCorpusReader(train_path, '.*', cat_pattern='(\w*)')

# Get categories
print '%d categories: %s' % (len(cr.categories()), ', '.join(cr.categories()))

for c in [cr.categories()[0]]:
    print c + '...'
    sys.stdout.flush()
    
    ngrams = {}
    for i in range(n, 0, -1):
        print str(i) + '-grams...'
        ngrams[i] = {}
        prefix = ('',) * (i - 1)
        for ngram in ingrams(chain(prefix, cr.words(categories=[c])), n):
            if not ngram in ngrams[i]:
                ngrams[i][ngram] = 0
            
            ngrams[i][ngram] += 1
    
    print ngrams
    

sys.exit()


total_words = len(cr.words())
cat_prob_dict = {}
ngrams = {}

for c in cr.categories():
    print c, '...'
    sys.stdout.flush()
    
    ngrams[c] = SLINgramModel(3, cr.words(categories=[c]))
    
    ngrams[c].weight = 0.5
    ngrams[c]._backoff.weight = 0.3
    ngrams[c]._backoff._backoff.weight = 0.2
    
    file = open(os.path.join(train_path, c + '.p'), 'w')
    pickle.dump(ngrams[c], file)
    
    nw = len(cr.words(categories=[c]))
    
    cat_prob_dict[c] = float(nw) / float(total_words)
    
    
    #nw = len(cr.words(categories=[c]))
    #ns = len(cr.sents(categories=[c]))
    #np = len(cr.paras(categories=[c]))
    #print '%s: #words: %d, #sents: %d, #paras: %d' % (c, nw, ns, np)
    


cat_prob_dist = DictionaryProbDist(cat_prob_dict, normalize=True)
file = open(os.path.join(train_path, 'categories.p'))
pickle.dump(cat_prob_dist, file)


# Corpus loaded

'''
Construct trigrams, bigrams and unigrams models for each category
- Count frequencies!

Now what?

We would like to estimate P(topic_i | D)

Naive Bayes:

P(topic_i | D) = P(D | topic_i) * P(topic_i)        = P(D | topic_i) * P(topic_i)
                ----------------------------
                        P(D) <-- can be discarded


P(D | topic_i) = product_{i=1}^n: P(w_i | topic_i)        ???
                                        ^
                                    from n-gram model 

P(topic_i) = #words in topic_i / #total words                     ???

'''

if __name__ == '__main__':
    from nltk import bigrams
    from nltk.corpus import brown, reuters
    from corpus import FreqDist
    
    bs = bigrams(word.lower() for word in brown.words() + reuters.words() if word.isalpha())
    fdist = FreqDist(bs)
    print fdist.dumps()
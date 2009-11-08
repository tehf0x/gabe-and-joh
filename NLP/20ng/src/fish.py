'''
Created on 6 Nov 2009

@author: joh
'''

import os
import sys
import cPickle as pickle

#from nltk import trigrams, word_tokenize, sent_tokenize, FreqDist
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader
from nltk.probability import DictionaryProbDist
from nltk.model import NgramModel
from nltk.classify import NaiveBayesClassifier

from model import SLINgramModel

train_path = 'data/task1_train'

cr = CategorizedPlaintextCorpusReader(train_path, '.*', cat_pattern='(\w*)')

# Get categories
print 'Categories:', ', '.join(cr.categories())

total_words = len(cr.words())
cat_prob_dict = {}
ngrams = {}

for c in [cr.categories()[0]]:
    print c, '...'
    sys.stdout.flush()
    
    ngrams[c] = SLINgramModel(3, cr.words(categories=[c]))
    
    ngrams[c].weight = 0.5
    ngrams[c]._backoff.weight = 0.3
    ngrams[c]._backoff._backoff.weight = 0.2
    
    #file = open(os.path.join(train_path, c + '.p'), 'w')
    #pickle.dump(ngrams[c], file)
    
    nw = len(cr.words(categories=[c]))
    
    cat_prob_dict[c] = float(nw) / float(total_words)
    
    
    #nw = len(cr.words(categories=[c]))
    #ns = len(cr.sents(categories=[c]))
    #np = len(cr.paras(categories=[c]))
    #print '%s: #words: %d, #sents: %d, #paras: %d' % (c, nw, ns, np)
    


cat_prob_dist = DictionaryProbDist(cat_prob_dict, normalize=True)
#file = open(os.path.join(train_path, 'categories.p'))
#pickle.dump(cat_prob_dist, file)


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
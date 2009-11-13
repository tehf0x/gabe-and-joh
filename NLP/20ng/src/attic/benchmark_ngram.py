'''
Created on 8 Nov 2009

@author: joh
'''

import sys
from time import time
from itertools import chain
import cPickle as pickle


from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader
from nltk.probability import ConditionalProbDist, ConditionalFreqDist, MLEProbDist
from nltk.util import ingrams


print 'Loading corpus...',
t = time()

train_path = 'data/task1_train'
cr = CategorizedPlaintextCorpusReader(train_path, '.*', cat_pattern='(\w*)')

t = time() - t
print str(t) + 's'

# Test generation of CFD
print 'Creating CFD...',
sys.stdout.flush()
t = time()

cat = cr.categories()[0]

n = 3

cfd = ConditionalFreqDist()
prefix = ('',) * (n - 1)

for ngram in ingrams(chain(prefix, cr.words(categories=[cat])), n):
    context = tuple(ngram[:-1])
    token = ngram[-1]
    cfd[context].inc(token)

t = time() - t
print str(t) + 's'


t = time()
print 'Pickling CFD...',
sys.stdout.flush()

pickle.dump(cfd, open('cfd.p', 'w'), protocol=1)

t = time() - t
print str(t) + 's'


t = time()
print 'Loading pickled CFD...',
sys.stdout.flush()

cfd = pickle.load(open('cfd.p', 'r'))

t = time() - t
print str(t) + 's'



# Test generation of CPD
print 'Creating probdist...',
sys.stdout.flush()
t = time()

estimator = lambda fdist, bins: MLEProbDist(fdist)
cpd = ConditionalProbDist(cfd, estimator, len(cfd))

t = time() - t
print str(t) + 's'

t = time()
print 'Pickling probdist...',
sys.stdout.flush()

pickle.dump(cpd, open('cpd.p', 'w'), protocol=1)

t = time() - t
print str(t) + 's'


t = time()
print 'Loading pickled probdist...',
sys.stdout.flush()

cpd = pickle.load(open('pd.p', 'r'))

t = time() - t
print str(t) + 's'






print 'Creating count dict...',
sys.stdout.flush()
t = time()

cat = cr.categories()[0]

n = 3

cfd = dict()
prefix = ('',) * (n - 1)

for ngram in ingrams(chain(prefix, cr.words(categories=[cat])), n):
    context = tuple(ngram[:-1])
    token = ngram[-1]
    
    if not context in cfd:
        cfd[context] = dict()
    if not token in cfd[context]:
        cfd[context][token] = 0
    
    cfd[context][token] += 1

t = time() - t
print str(t) + 's'


t = time()
print 'Pickling count dict...',
sys.stdout.flush()

pickle.dump(cfd, open('cfdict.p', 'w'), protocol=1)

t = time() - t
print str(t) + 's'


t = time()
print 'Loading pickled count dict...',
sys.stdout.flush()

cfd = pickle.load(open('cfdict.p', 'r'))

t = time() - t
print str(t) + 's'




print 'Counting ngrams...',
sys.stdout.flush()
t = time()

cat = cr.categories()[0]

n = 3

freq = dict()

for ngram in ingrams(cr.words(categories=[cat]), n):
    if ngram not in freq:
        freq[ngram] = 0
    
    freq[ngram] += 1

t = time() - t
print str(t) + 's'


t = time()
print 'Pickling ngram counts...',
sys.stdout.flush()

pickle.dump(freq, open('ngram_freq.p', 'w'), protocol=1)

t = time() - t
print str(t) + 's'


t = time()
print 'Loading pickled ngram counts...',
sys.stdout.flush()

tmp = pickle.load(open('ngram_freq.p', 'r'))

t = time() - t
print str(t) + 's'


t = time()
print 'Saving ngram counts as text...',
sys.stdout.flush()

file = open('ngram_freq.txt', 'w')

for ngram, count in freq.items():
    s = ' '.join(ngram) + '\t' + str(count) + '\n'
    file.write(s)

file.close()

t = time() - t
print str(t) + 's'


t = time()
print 'Loading ngram counts text...',
sys.stdout.flush()

file = open('ngram_freq.txt', 'r')
tfreq = dict()

for line in file:
    parts = line.split()
    ngram = tuple(parts[:-1])
    count = parts[-1]
    tfreq[ngram] = count

file.close()


cfd = pickle.load(open('ngram_freq.p', 'r'))

t = time() - t
print str(t) + 's'

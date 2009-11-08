"""
NgramModel with Simple Linear Interpolation

@author: joh
"""

from itertools import chain

from nltk.model import NgramModel
from nltk.probability import ConditionalProbDist, ConditionalFreqDist, MLEProbDist
from nltk.util import ingrams

class SLINgramModel(NgramModel):
    """
    NgramModel with Simple Linear Interpolation for unseen n-grams
    
    
    """
    
    # TODO: Estimate this with EM
    weight = 0.3
    
    # add cutoff
    def __init__(self, n, train, estimator=None):
        """
        Creates an ngram language model to capture patterns in n consecutive
        words of training text.  An estimator smooths the probabilities derived
        from the text and may allow generation of ngrams not seen during
        training.

        @param n: the order of the language model (ngram size)
        @type n: C{int}
        @param train: the training text
        @type train: C{list} of C{string}
        @param estimator: a function for generating a probability distribution
        @type estimator: a function that takes a C{ConditionalFreqDist} and
              returns a C{ConditionalProbDist}
        """
        
        self._n = n

        if estimator is None:
            estimator = lambda fdist, bins: MLEProbDist(fdist)

        cfd = ConditionalFreqDist()
        self._ngrams = set()
        self._prefix = ('',) * (n - 1)

        for ngram in ingrams(chain(self._prefix, train), n):
            self._ngrams.add(ngram)
            context = tuple(ngram[:-1])
            token = ngram[-1]
            cfd[context].inc(token)

        self._model = ConditionalProbDist(cfd, estimator, len(cfd))

        # recursively construct the lower-order models
        if n > 1:
            self._backoff = SLINgramModel(n-1, train, estimator)
    
    # SLI probability
    def prob(self, word, context):
        """
        Evaluate the probability of this word in this context.
        """

        context = tuple(context)
        
        p = self[context].prob(word)
        
        
        print str(self._n) + '-gram:', repr(word), 'in context', context, '=', p
        
        if self._n > 1:
            p += self._backoff.prob(word, context[1:])
        
        return p
    
    
    def export(self):
        """
        Export this ngram model to a serializable object
        """
        o = dict()
        o['n'] = self._n
        o['ngrams'] = self._ngrams
        
    
    def dump(self, file):
        """
        Dump model data to file
        """
        
        ngrams = {}
        
        
    
    
    
    
    
    
    
    
    
    
    
    
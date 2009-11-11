"""
Language Model for document classification

Uses an n-gram model with Simple Linear Interpolation

@author: joh
"""

from math import log
from itertools import chain
import logging

from nltk.model import NgramModel
from nltk.probability import ProbDistI, ConditionalProbDist, ConditionalFreqDist, \
                             MLEProbDist, DictionaryProbDist, LaplaceProbDist
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader
from nltk.classify import NaiveBayesClassifier
from nltk.classify import ClassifierI
from nltk.util import ingrams

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('model')

class DocumentClassifier(ClassifierI):
    
    def __init__(self, lang_model):
        self.model = lang_model
        
        cond_probdist = dict(((c, 'text'), lang_model.ngram_probdists[c]) \
                             for c in lang_model.category_probdist.samples())
        
    def labels(self):
        """
        @return: the list of category labels used by this classifier.
        @rtype: C{list} of (immutable)
        """
        return self.model.category_probdist.samples()
    
    def classify(self, document):
        return self.prob_classify(document).max()
    
    def prob_classify(self, document):
        """
        @return: a probability distribution over labels for the given
            document.
        @rtype: L{ProbDistI <nltk.probability.ProbDistI>}
        """
        # Find the log probabilty of each label, given the features.
        # Start with the log probability of the label itself.
        logprob = {}
        
        for label in self.labels():
            logprob[label] = self.model.category_probdist.prob(label)
            ngram_model = self.model.ngrams[label]
            
            prefix = ('',) * (ngram_model._n - 1)
            words = [w.lower() for w in document if w.isalpha()]
            
            for ngram in ingrams(chain(prefix, words), 3):
                context = tuple(ngram[:-1])
                token = ngram[-1]
                #print token, context
                logprob[label] += -ngram_model.logprob(token, context)
            
            logger.debug(label + ': ' + str(logprob[label]))
        
        return DictionaryProbDist(logprob, normalize=True, log=True)

class LanguageModel(object):
    
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        
        # Load corpus
        logger.debug("Loading corpus from '" + corpus_path + "'...")
        
        self.corpus = CategorizedPlaintextCorpusReader(corpus_path, '.*', cat_pattern='(\w*)')
        
        # Count total number of words
        self.word_count = len(self.corpus.words())
        
        # Our category-conditional ngram models
        self.ngrams = dict()
        
        # Probability distribution for each ngram category
        self.ngram_probdists = dict()
        
        # Category probability dictionary
        cat_prob_dict = dict()
        
        # Loop through each category
        for c in self.corpus.categories():
            logger.debug("Processing category '" + c + "'...")
            
            # Create the NgramModel
            words = [w.lower() for w in self.corpus.words(categories=[c]) if w.isalpha()]
            self.ngrams[c] = SLINgramModel(3, words)
            
            # Set weights manually
            # TODO: Estimate with EM etc.
            self.ngrams[c].weight = 0.5
            self.ngrams[c]._backoff.weight = 0.3
            self.ngrams[c]._backoff._backoff.weight = 0.2
            
            # Create probdist
            self.ngram_probdists[c] = NgramProbDist(self.ngrams[c])
            
            # Count number of words in this category
            nw = len(self.corpus.words(categories=[c]))
            
            cat_prob_dict[c] = float(nw) / float(self.word_count)
            
        # Create category probability distribution
        self.category_probdist = DictionaryProbDist(cat_prob_dict, normalize=True)
    
    def prob(self, words, category):
        """ Compute the probability of words in category """
        
class NgramProbDist(ProbDistI):
    
    def __init__(self, ngram_model):
        self.model = ngram_model

    def logprob(self, words):
        """
        @return: the probability for a given sample.  Probabilities
            are always real numbers in the range [0, 1].
        @rtype: float
        @param sample: The sample whose probability
               should be returned.
        @type sample: any
        """
        prefix = ('',) * (self.model._n - 1)
        
        p = 0.0
        for ngram in ingrams(chain(prefix, words), self.model._n):
            context = tuple(ngram[:-1])
            token = ngram[-1]
            #print token, context
            d = self.model.logprob(token, context)
            logger.debug(token + ' in context ' + str(context) + ' = ' + str(d))
            if d > 0:
                p += float(d)
        
        return p

    def max(self):
        """
        @return: the sample with the greatest probability.  If two or
            more samples have the same probability, return one of them;
            which sample is returned is undefined.
        @rtype: any
        """
        raise AssertionError()

    # deprecate this (use keys() instead?)
    def samples(self):
        """
        @return: A list of all samples that have nonzero
            probabilities.  Use C{prob} to find the probability of
            each sample.
        @rtype: C{list}
        """
        raise AssertionError()
    

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
            estimator = lambda fdist, bins: LaplaceProbDist(fdist, bins)

        cfd = ConditionalFreqDist()
        self._ngrams = set()
        self._prefix = ('',) * (n - 1)

        for ngram in ingrams(chain(self._prefix, train), n):
            # Lowercase words
            ngram = tuple(w.lower() for w in ngram)
            self._ngrams.add(ngram)
            context = tuple(ngram[:-1])
            token = ngram[-1]
            cfd[context].inc(token)
        
        v = len(set(train))
        bins = v ** n
        
        self._model = ConditionalProbDist(cfd, estimator, bins)

        # recursively construct the lower-order models
        if n > 1:
            self._backoff = SLINgramModel(n-1, train, estimator)
    
    # SLI probability
    def prob(self, word, context):
        """
        Evaluate the probability of this word in this context.
        """
        word = word.lower()
        context = tuple(c.lower() for c in context)
        
        p = self[context].prob(word)
        
        
        #print str(self._n) + '-gram:', repr(word), 'in context', context, '=', p
        
        if self._n > 1:
            p += self._backoff.prob(word, context[1:])
        
        return p
    

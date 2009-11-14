"""
Language Model for document classification

Uses an n-gram model with Simple Linear Interpolation

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
"""

from math import log
from itertools import chain
import logging

from nltk.model import NgramModel
from nltk.probability import ProbDistI, ConditionalProbDist, ConditionalFreqDist, \
                             MLEProbDist, DictionaryProbDist, LaplaceProbDist
from nltk.util import ingrams

from probability import NeyProbDist

# Set up logger
logger = logging.getLogger('model')


class LanguageModel(object):
    """
    Language Model based on ngrams
    """

    def __init__(self, training_dict, factor=0.77):
        """
        training_dict: training data dictionary. Each element corresponds
                       to training data for one category.

        factor: The NeyProbDist smoothing factor
        """

        # Training data
        self.training_dict = training_dict

        # Count total number of words
        self.word_count = len(self.training_dict)

        # Our category-conditional ngram models
        self.ngrams = dict()

        # Category probability dictionary
        cat_prob_dict = dict()

        # Loop through each category
        for c,c_words in self.training_dict.items():
            logger.info("Processing category '" + c + "'...")

            words = [w.lower() for w in c_words if w.isalpha()]

            self.ngrams[c] = SLINgramModel(3, words, factor=factor)

            # Set weights manually
            # TODO: Estimate with EM etc.
            self.ngrams[c].weight = 0.5
            self.ngrams[c]._backoff.weight = 0.3
            self.ngrams[c]._backoff._backoff.weight = 0.2

            # Count number of words in this category
            nw = len(c_words)

            cat_prob_dict[c] = float(nw) / float(self.word_count)

        # Create category probability distribution
        self.category_probdist = DictionaryProbDist(cat_prob_dict, normalize=True)


class SLINgramModel(NgramModel):
    """
    NgramModel with Simple Linear Interpolation
    """

    # TODO: Estimate this with EM
    weight = 0.3

    def __init__(self, n, train, estimator=None, factor=0.77):
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
            if n > 1:
                # Use smoothing based on Ney et al
                probdist_factory = lambda fdist, bins, n_train, n_0: \
                                NeyProbDist(fdist, bins, n_train, n_0, factor, NeyProbDist.ABSOLUTE)
                                
                #probdist_factory = lambda fdist, bins, *args: LaplaceProbDist(fdist, bins)
            else:
                # Use simple add-1 smoothing for unigrams
                probdist_factory = lambda fdist, bins, *args: LaplaceProbDist(fdist, bins)
        else:
            probdist_factory = estimator

        # Initialize conditional frequency distribution
        cfd = ConditionalFreqDist()

        # Initialize set of ngrams
        self._ngrams = set()
        self._ngram_count = 0

        # Prefix beginning of document with empty strings
        self._prefix = ('',) * (n - 1)

        # Count the number of training examples
        num_training = 0

        # Loop through each ngram and add to CFD
        for ngram in ingrams(chain(self._prefix, train), n):
            # Lowercase words
            ngram = tuple(w.lower() for w in ngram)

            # Add to known ngrams
            self._ngrams.add(ngram)

            # Add to CFD
            context = tuple(ngram[:-1])
            token = ngram[-1]
            cfd[context].inc(token)

            num_training += 1

        # Calculate vocabulary size (for NeyProbDist)
        v = len(set(train))
        bins = v ** n

        # Number of bins with a count > 0
        self._ngram_count = len(self._ngrams)

        # Gives us number of bins with count = 0
        n_0 = bins - self._ngram_count

        # Create CPD model
        self._model = ConditionalProbDist(cfd, probdist_factory, bins, num_training, n_0)

        # recursively construct the lower-order models
        if n > 1:
            self._backoff = SLINgramModel(n-1, train, estimator)


    def prob(self, word, context):
        """
        Evaluate the probability of this word in this context.
        """
        word = word.lower()
        context = tuple(c.lower() for c in context)

        #if self._n == 1 and (word,) not in self._ngrams:
            # Unknown word!
        #    raise RuntimeError("No probability mass assigned to word %s in context %s" % (word, ' '.join(context)))

        # prob() should always return a smoothed non-zero probability
        p = self.weight * self[context].prob(word)

        # Add lower order ngram probabilities
        if self._n > 1:
            p += self._backoff.prob(word, context[1:])

        return p


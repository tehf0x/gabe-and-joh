"""
Document Classifier based on LanguageModel

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
"""
from itertools import chain
import logging

from nltk.classify import ClassifierI
from nltk.probability import DictionaryProbDist
from nltk.util import ingrams

# Set up logger
logger = logging.getLogger('classifier')

class DocumentClassifier(ClassifierI):
    """ Document classifier based on a language model """

    def __init__(self, lang_model):
        """
        lang_model = instance of model.LanguageModel
        """
        self.model = lang_model

    def labels(self):
        """
        @return: the list of category labels used by this classifier.
        @rtype: C{list} of (immutable)
        """
        return self.model.category_probdist.samples()

    def classify(self, document):
        """ Classify a document """
        return self.prob_classify(document).max()

    def prob_classify(self, document):
        """
        @return: a probability distribution over labels for the given document.
        @rtype: L{ProbDistI <nltk.probability.ProbDistI>}
        """
        # Find the log probabilty of each label, given the features.
        # Start with the log probability of the label itself.
        logprob = {}

        # Loop through each possible label and calculate the
        # (log) probability of document under that label
        for label in self.labels():
            # Probability of category
            logprob[label] = self.model.category_probdist.prob(label)

            # Extract ngram model
            ngram_model = self.model.ngrams[label]

            prefix = ('',) * (ngram_model._n - 1)

            # Prepare words
            words = [w.lower() for w in document if w.isalpha()]

            # Go through each word and calculate P(w | context)
            for ngram in ingrams(chain(prefix, words), ngram_model._n):
                context = tuple(ngram[:-1])
                token = ngram[-1]

                try:
                    logprob[label] += -ngram_model.logprob(token, context)
                except RuntimeError:
                    # Unknown word, skip it
                    #logger.debug(label + ': Ignoring unknown word: ' + token)
                    continue

            #logger.debug(label + ': ' + str(logprob[label]))

        # Return probability for each label
        return DictionaryProbDist(logprob, normalize=True, log=True)


def test(classifier, corpus, test_files = None, progress=None):
    """
    classifier = instance of nltk.classify.ClassifierI
    corpus = instance of nltk.corpus.reader.plaintext.CategorizedCorpusReader
    """
    if not test_files:
        # Default to testing the entire corpus
        test_files = dict((c, corpus.fileids(categories=[c])) for c in corpus.categories())

    # Initialize confusion matrix
    labels = classifier.labels()
    confusion = dict((l, dict((l, 0) for l in labels)) for l in test_files.keys())

    # Classify every file
    if progress is not None:
        num_files = 0
        for files in test_files.values():
            num_files += len(files)
    cur_pos = 0
    for label, files in test_files.items():
        for fileid in files:
            l = classifier.classify(corpus.words(fileids=[fileid]))
            confusion[label][l] += 1
            #logger.info(fileid + ' => ' + l + '!')
            if progress is not None:
                cur_pos += 1
                progress(cur_pos, num_files)

    return confusion

def accuracy(confusion):
    """
    Calculate the accuracy from a confusion matrix.
    """
    accuracy = 0.0

    for l,r in confusion.items():
        accuracy += float(r[l]) / sum(r.values())

    return accuracy / len(confusion)

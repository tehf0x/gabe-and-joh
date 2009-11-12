"""
Test document classifier

@author: joh
"""
import logging

logger = logging.getLogger('test-classifier')

def test_classifier(classifier, corpus):
    """
    classifier = instance of nltk.classify.ClassifierI
    corpus = instance of nltk.corpus.reader.plaintext.CategorizedCorpusReader
    """
    # Initialize confusion matrix
    labels = classifier.labels()
    confusion = dict((l, dict((l, 0) for l in labels)) for l in labels)
    
    for label in corpus.categories():
        for fileid in corpus.fileids(categories=[label]):
            l = classifier.classify(corpus.words(fileids=[fileid]))
            confusion[label][l] += 1
            logger.info(label + ': ' + fileid + ' => ' + l + '!')
    
    return confusion

if __name__ == '__main__':
    pass
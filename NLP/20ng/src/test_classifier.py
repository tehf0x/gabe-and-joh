"""
Test document classifier

@author: joh
"""
import logging

logger = logging.getLogger('test-classifier')

def test_classifier(classifier, corpus, test_files):
    """
    classifier = instance of nltk.classify.ClassifierI
    corpus = instance of nltk.corpus.reader.plaintext.CategorizedCorpusReader
    """
    # Initialize confusion matrix
    labels = classifier.labels()
    confusion = dict((l, dict((l, 0) for l in labels)) for l in test_files.keys())

    for label, files in test_files.items():
        for fileid in files:
            l = classifier.classify(corpus.words(fileids=[fileid]))
            confusion[label][l] += 1
            logger.info(label + ': ' + fileid + ' => ' + l + '!')

    return confusion

def calc_accuracy(confusion):
    '''
    Calculate the accuracy froma confusion matrix.
    '''
    accuracy = 0.0

    for l,r in confusion.items():
        accuracy += float(r[l]) / sum(r.values())

    return accuracy / len(confusion)


if __name__ == '__main__':
    pass

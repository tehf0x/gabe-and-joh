'''
Run the CV10 for finding the good k-value.
'''

from model import *
from test_classifier import *

#Define some constants
num_slices = 10


def extract_slice(corpus, slice_pos):
    '''
    Returns a training dict and a test dict.
    '''
    training_files = {}
    test_files = {}
    for category in corpus.categories():
        file_list = corpus.fileids(categories=[category])
        width = len(file_list) / num_slices
        start = slice_pos * width
        end = start + width

        training_files[category] = file_list[:start] + file_list[end:]
        test_files[category] = file_list[start:end]


    #print [(c, len(v)) for c,v in training_files.items()]

    return (training_files, test_files)


corpus = CategorizedPlaintextCorpusReader('data/task1_train', '.*', cat_pattern='(\w*)')

max_accuracy = 0
best_factor = -1

for t_factor in range(0,4):
    accuracy = 0
    factor = t_factor/10.0

    for s in range(0,10):
        training_dict = {}

        training_files, test_files = extract_slice(corpus, s)

        #print training_files, test_files

        for category, files in training_files.items():
            training_dict[category] = corpus.words(fileids=files)

        m = LanguageModel(training_dict, factor=factor)
        c = DocumentClassifier(m)

        confusion = test_classifier(c, corpus, test_files)
        accuracy += calc_accuracy(confusion)

        del c
        del m

    print "Factor: %f, Accuracy: %f." % (factor, accuracy)
    if accuracy > max_accuracy:
        best_factor = factor
        max_accuracy = accuracy

print "Best Factor: %f with accuracy %f" % (best_factor, max_accuracy)


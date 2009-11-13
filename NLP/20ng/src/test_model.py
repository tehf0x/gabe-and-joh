#!/usr/bin/env python
"""
Test the language model in document classification tasks

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
"""

if __name__ == '__main__':
    from sys import argv, stderr, exit
    import logging
    from optparse import OptionParser
    
    parser = OptionParser(usage="Usage: %prog [-v] <train-dir> <test-dir>")
    parser.add_option('-v', '--verbose', 
                      action="store_true", default=False, dest='verbose',
                      help="Verbose output")
    
    (opts, args) = parser.parse_args()
    
    if len(args) < 2:
        parser.error('Not enough arguments')
    
    train_dir = args[0]
    test_dir = args[1]
    
    from nltk.corpus import *
    from model import *
    from classify import *
    
    # Suppress some output
    if opts.verbose:
        logging.basicConfig(level=logging.INFO)
    
    # Load corpus
    print "Loading training corpus from '%s'..." % (train_dir)
    train_corpus = CategorizedPlaintextCorpusReader(train_dir, '.*', cat_pattern='([^/]*)')
    train_dict = dict((c, train_corpus.words(categories=[c])) for c in train_corpus.categories())
    
    print "Loading test corpus from '%s'..." % (test_dir)
    test_corpus = CategorizedPlaintextCorpusReader(test_dir, '.*', cat_pattern='([^/]*)')
    
    # Train model
    print "Constructing Language Model... (this might take a while)"
    m = LanguageModel(train_dict)
    c = DocumentClassifier(m)
    
    # Classify documents
    print "Testing model against test corpus... (this might also take a while)"
    
    confusion = test(c, test_corpus)
    
    print
    print "Confusion Matrix:\n"
    
    lw = max([len(l) for l in confusion.keys()])
    
    print (' ' * (lw + 1)),
    for l in confusion.values()[0].keys():
        print '%s ' % (l),
    print
    
    for l, r in confusion.items():
        print l.ljust(lw + 1),
        
        for k, v in r.items():
            print '%s ' % (str(v).rjust(len(k))),
        
        print
    print
    
    acc = accuracy(confusion)
    print "Accuracy: %2.2f%%" % (acc * 100)
    
    
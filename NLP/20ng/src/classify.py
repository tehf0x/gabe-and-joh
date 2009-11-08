'''
Classify documents.

Gabe Arnold <gabe@squirrelsoup.net>
'''

from nltk import NaiveBayesClassifier
from optparse import OptionParser

#Set up a couple CLI options.
parser = OptionParser()
parser.add_option('-f', '--file', dest='filename')

(opts, args) = parser.parse_args()

#Read in the filenames either from a line-by-line text file of the names,
#or by all the names being on the CLI
file_names = []
if opts.filename is None:
    file_names = args
else:
    f = open(opts.filename)
    file_names = [fname.strip() for fname in f]

#Create the bayes classifier:
nb_classifier = NavieBayesClassifier(label_pd, feature_pd)

class_results = {}
#Now classify each file into the alloted class:
for file_name in file_names:
    f = open(file_name)
    contents = f.read()
    featureset = {'document' : contents}
    label = nb_classifier.classify(featureset)
    class_results[file_name] = label

print class_results

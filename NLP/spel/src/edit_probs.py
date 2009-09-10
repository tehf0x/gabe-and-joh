'''
Created on Sep 8, 2009

@author: garnold
'''

import nltk
import permutate
import corpus
import pickle

from copy import copy
from dictionary import Dictionary
from nltk.corpus import reuters

#This comes in handy:
alphabet = 'abcdefghijklmnopqrstuvwxyz@'
#Dictionary for lookups.
dt = Dictionary()

"""
Confusion matrices for various edits.
It's necessary to keep the 'types' var around to re-iterate through the
dictionary while editing it.
"""
types = ('delete', 'transpose', 'replace', 'insert')
container = dict((type, {}) for type in types)

#Default occurrences to 0
for type in types:
    container[type] = dict((i, dict((c,0) for c in alphabet)) for i in alphabet)

def get_unusual():
    dict_path = '/etc/dictionaries-common/words'
    f= open(dict_path)
    dict_words = f.read().split()
             
    text_vocab = set(w.lower() for w in reuters.words() if w.isalpha())
    #print sorted(text_vocab)
    english_vocab = set(w.lower() for w in dict_words if w.isalpha())
    english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.words.words()))
    #print sorted(english_vocab)
    unusual = text_vocab.difference(english_vocab)
    return unusual

def update_cmatrix(edit):
    container[edit[0]][edit[1]][edit[2]] += 1
    
unusual = ('zoomd',)

for word in get_unusual():
    perms = dict((perm, meta) for (perm,meta) in permutate.permutate_meta(word))
    edits = {}
    print word
    for perm in perms:
        if dt.has_word(perm):
            edits[perm] = perms[perm]
    if len(edits) == 0:
        continue
    print edits
    just_words = edits.keys()
    c_word = corpus.freq_sort(just_words)[0]
    correction = c_word, edits[c_word]
    print correction
    update_cmatrix(edits[c_word])

print container['insert']['m']
#print get_unusual()

pickle.dump(container, open('conf_matrix.pickle', 'w'))


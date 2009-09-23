'''
Created on Sep 8, 2009

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''

import nltk
import permutate
import pickle
import corpus

#Dictionary for lookups.
from dictionary import Dictionary
from nltk.corpus import reuters

class ConfusionMatrix():
    '''
    Confusion matrices for various edits.
    It's necessary to keep the 'types' var around to re-iterate through the
    dictionary while editing it.
    '''
    
    types = ('delete', 'transpose', 'replace', 'insert')
    alphabet = 'abcdefghijklmnopqrstuvwxyz@'

    def __init__(self, pickle_name = 'data/conf_matrix.pickle', no_load = False):
        '''
        Load the confusion matrices from pickle_name, and if no pickle is found,
        generate the confusion matrices.
        '''
        self.dt = Dictionary()
        self.container = dict()
        self.letter_freq = dict()
        
        #Don't load the pickle, in case we want to run some tests, debug etc.
        if no_load:
            return None

        try:
            fh = open(pickle_name, 'r')
            print 'Loading confusion matrix from "%s"...' % (pickle_name) 
            self.container, self.letter_freq = pickle.load(fh)
        
        except IOError:
            # File not found, generate
            print 'Generating corpus to "%s"... This can take some time...' % (pickle_name)
            self.container = dict((type, {}) for type in self.types)
            for type in self.types:
                self.container[type] = dict((i, dict((c,0) for c in self.alphabet)) 
                                            for i in self.alphabet)
            self.construct_matrix()
            self.construct_freq()
            pickle.dump((self.container, self.letter_freq), open(pickle_name, 'w'))
            
    def get_unusual(self):
        #List of words in the text
        text_vocab = set(w.lower() for w in reuters.words() if w.isalpha())
        #List of words in the dictionary
        english_vocab = set(w.lower() for w in self.dt.words if w.isalpha())
        #(text_vocab - english_vocab) = misspelled words
        return text_vocab.difference(english_vocab)

    def update_cmatrix(self,edit):
        self.container[edit[0]][edit[1]][edit[2]] += 1
    
    def construct_freq(self, text = None):
        if text == None:
            from nltk.corpus import reuters
            text = reuters.raw()
        #Get rid of \n
        c_text = text.replace('\n','')
        self.letter_freq = nltk.FreqDist(c_text)
        for bigram in nltk.bigrams(c_text):
            self.letter_freq.inc(''.join(bigram))
        
    def construct_matrix(self, word_list = None, dictionary = None):
        '''
        This goes through the text, and for every word that is not a dictionary
        word, it runs a noisy channel on the word, figures out the correction
        candidates, and then updates the transformation table with the transformation
        that took place for the most likely candidate word (based on P(c)).
        '''
        freq_dist = corpus.FreqDist()
        freq_dist.load(open('data/count_brown.txt'))
        if word_list == None:
            word_list = self.get_unusual()
        if dictionary == None:
            dictionary = self.dt
        
        for word in word_list:
            #Load up all the permutations possible, along with what permutation took place:
            perms = dict((perm, meta) for (perm,meta) in permutate.permutate_meta(word))
            edits = {}
            for perm in perms:
                if dictionary.has_word(perm):
                    edits[perm] = perms[perm]
            if len(edits) == 0:
                continue
            just_words = edits.keys()
            #Get the most likely word according to the word probability
            c_word = freq_dist.sort_samples(just_words)[0]
            correction = c_word, edits[c_word]
            self.update_cmatrix(edits[c_word])

    def get_prob(self, permutation):
        '''
        These differ slightly from the paper describing the probability
        calculations.  Here we have have 'insert' as calculated 'from a typo to
        a correct word', which is equivalent to a delete 'from a correct word to
        a typo'.  The paper considered all the mutations to be from a correct 
        word to a typo.
        '''
        try:
            if permutation[0] in ('insert', 'transpose'):
                return (float(self.container[permutation[0]][permutation[1]][permutation[2]]) /
                        float(self.letter_freq[permutation[1] if permutation[1] != '@' 
                                               else '' + permutation[2]]))
            elif permutation[0] == 'delete':
                return (float(self.container[permutation[0]][permutation[1]][permutation[2]]) /
                        float(self.letter_freq[permutation[1] if permutation[1] != '@' 
                                               else permutation[2]]))
            elif permutation[0] == 'replace':
                return (float(self.container[permutation[0]][permutation[1]][permutation[2]]) /
                        float(self.letter_freq[permutation[2]]))
        
        except ZeroDivisionError:
            return 0.0  


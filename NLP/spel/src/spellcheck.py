'''
Spellcheck module

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
'''

import nltk
from nltk import sent_tokenize, word_tokenize

from dictionary import Dictionary
from permutate import permutate
from util import CaseMask
import corpus 

# Our dictionary
dictionary = Dictionary()

class SpellcheckResult(object):
    ''' Spelling error result '''
    
    def __init__(self, sentence, word_pos, candidates = []):
        self.sentence = sentence
        self.word_pos = word_pos
        self.word = sentence[word_pos]
        self.candidates = candidates
    
    def context(self, before = 2, after = 2):
        ''' Get the context around the word '''
        before = abs(before)
        after = abs(after)
        
        if self.word_pos - before < 0:
            before = self.word_pos
        
        if self.word_pos + after >= len(self.sentence):
            after = len(self.sentence) - self.word_pos
        
        return self.sentence.tokens[self.word_pos - before : self.word_pos + after + 1]
    
    def __repr__(self):
        return '<SpellcheckResult: word "%s", #%d in "%s", candidates: %s>' % (self.word, self.word_pos, ' '.join(self.context()), self.candidates)
 

class Spellcheck(object):
    '''
    Spellchecker class which can process an abritrary text
    '''
    stored_results = None
    
    def __init__(self, text):
        self.raw = text
        self.sents = [nltk.Text(word_tokenize(sent)) for sent in sent_tokenize(text)]
        self.words = nltk.Text(word_tokenize(text))
    
    
    
    def results(self):    
        sent_results = {}
        for i, sentence in enumerate(self.sents):
            for word_pos, word in enumerate(sentence):
                # Skip non-alphanumeric characters -- TODO: how to deal with this?
                if not word.isalpha():
                    continue
                
                # Keep case mask and lowercase word
                mask = CaseMask(word)
                word = word.lower()
                
                # Check if word is in our dictionary
                if dictionary.has_word(word):
                    continue
                
                # Create permutations of word
                permutations = permutate(word)
                
                # Find permutations in dictionary
                dict_cands = set([w for w in permutations if dictionary.has_word(w)])
                dict_cands = corpus.freq_sort(dict_cands)
                
                # Find permutations in corpus
                corpus_cands = corpus.known(permutations - set(dict_cands))
                corpus_cands = corpus.freq_sort(corpus_cands)
                
                candidates = map(mask.apply, list(dict_cands) + list(corpus_cands))
                
                result = SpellcheckResult(sentence, word_pos, candidates)
                
                if not sent_results.has_key(i):
                    sent_results[i] = []
                
                sent_results[i].append(result)
        
        return sent_results
        #return self.stored_results
        
        
        
        
        
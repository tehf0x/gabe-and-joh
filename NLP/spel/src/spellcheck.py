'''
Spellcheck module

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
'''

import copy
import nltk
from nltk import sent_tokenize, word_tokenize

from dictionary import Dictionary
from permutate import edits
from util import CaseMask
import corpus 
from corpus import FreqDist

# Our dictionary
#dictionary = Dictionary()


class Spellchecker(object):
    """ Spellchecker which can process an arbitrary text """
    
    
    def __init__(self, max_edit_distance=2, dictionary=Dictionary(), word_counts="data/count_brown.txt"):
        """ Create a new Spellchecker
        
        Keyword arguments:
        max_edit_distance -- Maximum edit distance we should consider for words.
                             Anything above 2 is too computationally intensive for most systems.
        
        dictionary -- Dictionary to use
        word_counts -- Filename of word counts file
        """
        self.max_edit_distance = max_edit_distance
        self.dictionary = dictionary
        self.freq = FreqDist()
        self.freq.load(open(word_counts))
    
    def check(self, text):
        """ Check a text for spelling errors
        
        Returns a SpellcheckResult with information about misspelled words
        and candidates.
        """
        sents = [word_tokenize(sent) for sent in sent_tokenize(text)]
        
        results = SpellcheckResult(sents)
        
        # Loop through sentences, words
        for sentence_pos, sentence in enumerate(sents):
            for word_pos, word in enumerate(sentence):
                # Skip non-alphanumeric characters -- TODO: how to deal with this?
                if not word.isalpha():
                    continue
                
                # Keep case mask and lowercase word
                mask = CaseMask(word)
                word = word.lower()
                
                # Check if word is in our dictionary
                if self.dictionary.has_word(word):
                    continue
                
                for n in range(1, self.max_edit_distance + 1):
                    # Make a list of candidates of distance N
                    word_edits = edits(n, word)
                    
                    # Find words that are in dictionary
                    dict_cands = set([w for w in word_edits if self.dictionary.has_word(w)])
                    dict_cands = self.freq.sort_samples(dict_cands)
                    
                    # Find unknown words from corpus
                    corpus_cands = self.freq.known(word_edits - set(dict_cands))
                    corpus_cands = self.freq.sort_samples(corpus_cands)
                    
                    # Candidates in dictionary get favored
                    candidates = list(dict_cands) + list(corpus_cands)
                    
                    if candidates:
                        # Found candidates, don't try any larger edit distance
                        break
                
                
                # Apply case mask to candidates
                candidates = map(mask.apply, candidates)
                
                # Add result
                result = Correction(mask.apply(word), candidates, sentence_pos, word_pos)
                results.append(result)
        
        return results
    
    def correct(self, text):
        """ Correct misspelled word in text.
        Returns the corrected text. """
        raise NotImplementedError
    




class SpellcheckResult(list):
    """ Result of a spellcheck. """
    
    def __init__(self, sents=None, corrections=[]):
        self.sents = sents
        self.extend(corrections)
    
    def __repr__(self):
        return '<SpellcheckResult: %d sentences with %d corrections>' % (len(self.sents), len(self))
    
    def corrected(self):
        """ Get the corrected text sentences """
        sents = copy.deepcopy(self.sents)
        
        for c in self:
            if c.candidates:
                sents[c.sentence_pos][c.word_pos] = c.candidates[0]
        
        return sents


class Correction(object):
    """ Contains information about a single spelling correction """
    
    def __init__(self, word, candidates=[], sentence_pos=0, word_pos=0):
        """ Create a word correction.
        
        Keyword arguments:
        word -- the original word
        candidates -- a list of candidate corrections of word, ordered
                      by likeliness.
        sentence_pos -- the position of the sentence in the text
        word_pos -- the position of the word in the sentence
        """
        self.word = word
        self.candidates = candidates
        self.sentence_pos = sentence_pos
        self.word_pos = word_pos
    
    def __repr__(self):
        return '<Correction: %s: %s>' % (self.word, ' '.join(self.candidates))



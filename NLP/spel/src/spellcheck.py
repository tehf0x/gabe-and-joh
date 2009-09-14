'''
Spellcheck module

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
'''

import copy
import nltk
from nltk import sent_tokenize, word_tokenize

from dictionary import Dictionary
from permutate import edits_meta
from util import CaseMask, normalize
import corpus 
from corpus import FreqDist
from edit_probs import ConfusionMatrix

# Our dictionary
#dictionary = Dictionary()


class Spellchecker(object):
    """ Spellchecker which can process an arbitrary text """
    
    
    def __init__(self, max_edit_distance=2, dictionary=Dictionary(), 
                 word_counts="data/count_brown.txt", bigram_counts="data/count_2w_brown_reuters.txt"):
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
        
        self.bfreq = FreqDist()
        self.bfreq.load(open(bigram_counts))
        
        self.cmatrix = ConfusionMatrix()
    
    def prob(self, word, edit, context=None):
        """ Calculate probability of candidate word given edit info
        and context = (word_before, None) | (None, word_after) | (word_before, word_after)
        """
        p_word = self.freq.freq(word)
        p_edit = self.cmatrix.get_prob(edit)
        p_context = 1
        
        if context:
            word_before, word_after = context
            
            if word_before or word_after:
                if word_before:
                    p_context += self.bfreq[(word_before, word)]
                if word_after:
                    p_context += self.bfreq[(word, word_after)]
        
        return p_word * p_edit * p_context
    
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
                
                # Determine context
                word_before = word_after = None
                if word_pos > 0:
                    word_before = sentence[word_pos - 1]
                if word_pos < len(sentence) - 1:
                    word_after = sentence[word_pos + 1]
                context = (word_before, word_after)
                
                for n in range(1, self.max_edit_distance + 1):
                    # Make a list of candidates of distance N
                    # edits_meta -> (word, (meta))
                    word_edits = edits_meta(n, word)
                    
                    # Find words that are in dictionary
                    dict_cands = set([w for w in word_edits if self.dictionary.has_word(w[0])])
                    
                    # Find unknown words from corpus
                    non_words = word_edits - dict_cands
                    #non_words = set([w for w in word_edits if not w[0] in cands])
                    corpus_cands = set([w for w in non_words if self.freq.has_key(w[0])])
                    
                    cands = dict_cands.union(corpus_cands)
                    
                    # Calculate probabilities for each candidate
                    # dict_cands: word -> probability
                    probs = {}
                    for cand in cands:
                        w, edit = cand
                        p = self.prob(w, edit, context)
                        if probs.has_key(w):
                            probs[w] += p
                        else:
                            probs[w] = p
                    
                    # Normalize probabilities
                    if probs:
                        probs = normalize(probs)
                    
                    # Sort candidates
                    candidates = sorted(probs.keys(), 
                                        cmp = lambda c1, c2: cmp(probs[c1], probs[c2]),
                                        reverse = True)
                    
                    if candidates:
                        # Found candidates, don't try any larger edit distance
                        break
                
                
                # Apply case mask to candidates
                candidates = map(mask.apply, candidates)
                
                # Add result
                result = Correction(mask.apply(word), candidates, probs, sentence_pos, word_pos)
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
    
    def __init__(self, word, candidates=[], candidate_probs={}, sentence_pos=0, word_pos=0):
        """ Create a word correction.
        
        Keyword arguments:
        word -- the original word
        candidates -- a list of candidate corrections of word, ordered
                      by likeliness.
        sentence_pos -- the position of the sentence in the text
        word_pos -- the position of the word in the sentence
        cand_meta -- meta-information about each candidate
        """
        self.word = word
        self.candidates = candidates
        self.candidate_probs = candidate_probs
        self.sentence_pos = sentence_pos
        self.word_pos = word_pos
    
    def __repr__(self):
        return '<Correction: %s: %s>' % (self.word, ' '.join(self.candidates))



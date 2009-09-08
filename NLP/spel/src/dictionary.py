'''
Dictionary Lookup

Lookup a word in a dictionary to see if it is defined.
The dictionary is composed of a specified text file that will be used to 
complement the NLTK 'words' corpus.

Created on Sep 7, 2009

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''

from nltk.corpus import words

class Dictionary():
    
    def __init__(self, dict_path = '/etc/dictionaries-common/words'):
         f= open(dict_path)
         self.words = set(f.read().split()).union(words.words())
        
    def has_word(self, word):
        return word in self.words
    


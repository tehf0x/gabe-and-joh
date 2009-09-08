'''
Dictionary Lookup

Lookup a word in a specified dictionary to see if it is present.

Created on Sep 7, 2009

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''

class Dictionary():
    
    def __init__(self, dict_path = '/etc/dictionaries-common/words'):
        f = open(dict_path)
        self.words = f.read().split()
        
    def has_word(self, word):
        return self.words.count(word) == 1
    


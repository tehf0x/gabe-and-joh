'''
Utilities for spellchecker

Created on 10 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com
'''

from copy import copy

class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = value = self.func(*args)
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
        
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


class CaseMask(object):
    ''' A CaseMask is a mask for which letters of a word is of what case.
    It can be stored from one word and applied to another word '''
    
    def __init__(self, word):
        ''' Create a CaseMask of word '''
        self.mask = []
        
        for letter in word:
            if letter.isupper():
                self.mask.append(True)
            else:
                self.mask.append(False)
    
    def apply(self, word):
        ''' Apply this case mask to word '''
        word2 = list(word)
        
        for i in range(len(word2)):
            if i == len(self.mask):
                # Word is longer than mask
                break
            
            if self.mask[i]:
                word2[i] = word2[i].upper()
            else:
                word2[i] = word2[i].lower()
        
        return ''.join(word2)
    
'''
Word permutations

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
'''

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    """ Get a set of all possible edits of word of distance 1 """
    # Split word into two in all possible ways
    split = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    
    # Deletes one character
    deletes = [a + b[1:] for a, b in split if b]
    
    # Swaps two characters
    transposes = [a + b[1] + b[0] + b[2:] for a, b in split if len(b) > 1]
    
    # Replace character
    replaces = [a + c + b[1:] for a, b in split for c in alphabet]
    
    # Insert character
    inserts = [a + c + b for a, b in split for c in alphabet]
    
    # Remove duplicates by creating a set
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """ Get a set of all possible edits of word of distance 2 """
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

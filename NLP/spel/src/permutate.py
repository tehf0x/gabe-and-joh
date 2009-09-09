'''
Word permutations

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
'''

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def permutate_meta(word):
    """
    Get a set of all possible edits of word of distance 1, and return the
    edit type along with the word.
    """
    # Split word into two in all possible ways
    split = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    
    # Deletes one character
    deletes = [(a + b[1:], ('delete', a[-1] if len(a)>0 else '@', b[0])) 
               for a, b in split if b]
    
    # Swaps two characters
    transposes = [(a + b[1] + b[0] + b[2:], ('transpose', b[0], b[1])) 
                  for a, b in split if len(b) > 1]
    
    # Replace character
    replaces = [(a + c + b[1:], ('replace', b[0], c)) 
                for a, b in split for c in alphabet if b]
    
    # Insert character
    inserts = [ (a + c + b, ('insert', a[-1] if len(a)>0 else '@', c)) 
               for a, b in split for c in alphabet]
    
    # Remove duplicates by creating a set
    return set(deletes + transposes + replaces + inserts)

def permutate(word, meta = False):
    """ Get a set of all possible edits of word of distance 1"""
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


def permutate_2(word):
    """ Get a set of all possible edits of word of distance 2 """
    return set(e2 for e1 in permutate(word) for e2 in permutate(e1))

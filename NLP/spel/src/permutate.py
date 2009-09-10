'''
Word permutations

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
@author: Gabriel Arnold <gabe@squirrelsoup.net>
'''

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1_meta(word):
    """ Get a set of all possible word edits of distance 1, and return the
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
    # TODO: This is currently bugged and does not remove duplicates
    # properly because set() does not consider ('aa', ('insert', '@', 'a')) 
    # and ('aa', ('insert', 'a', 'a')) to be equal.
    return set(deletes + transposes + replaces + inserts)

def edits2_meta(word):
    """ Get a set of all possible word edits of distance 2, and return the
    edit type along with the word.
    """
    # TODO: Implement?
    raise NotImplementedError
    #return set(e2 for e1 in edits1_meta(word[0]) for e2 in edits1_meta(e1[0]))
 

def edits1(word):
    """ Get a set of all possible word edits of distance 1 """
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
    """ Get a set of all possible word edits of distance 2 """
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits(n, word):
    """ Get a set of all possible word edits of distance n """
    if n < 1:
        raise AttributeError('n >= 1')
    if n == 1:
        return edits1(word)
    else:
        return set(e2 for e1 in edits(n-1, word) for e2 in edits(n-1, e1))
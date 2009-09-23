"""
Test cases for Spel

Created on 10 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
"""

from spellcheck import Spellcheck
from dictionary import Dictionary

# spell-errors.txt contains common spelling mistakes
# each line is in the format:
# <correct>: <wrong1> [wrong2] ...
fh = open('spell-errors.txt')

n_right = 0
n_unknown = 0
n_wrong = 0
n_total = 0

dictionary = Dictionary()

for line in fh:    
    right, wrongs = line.split(':')
    wrongs = [w.strip() for w in wrongs.split(',')]
    
    print right + ':'
    
    for wrong in wrongs:
        if dictionary.has_word(wrong.lower()):
            continue
        
        n_total += 1
        
        sc = Spellcheck(wrong)
        guess = sc.corrected()[0][0]
        
        print '\t%s => %s\t' % (wrong, guess),
        
        if guess == right:
            print 'CORRECT!'
            n_right += 1
        elif guess == wrong:
            print 'UNKNOWN'
            n_unknown += 1
        else:
            n_wrong += 1
            print 'WRONG'
            
print 'RESULTS:'
print '%d words checked' % (n_total)
print '%d right (%.2f)' % (n_right, 100 * float(n_right) / float(n_total))
print '%d wrong (%.2f)' % (n_wrong, 100 * float(n_wrong) / float(n_total))
print '%d unknown (%.2f)' % (n_unknown, 100 * float(n_unknown) / float(n_total))




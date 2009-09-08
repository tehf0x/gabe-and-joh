#!/usr/bin/env python
'''
The Spel spellchecker

Spel reads sentences from standard input and highlights the
misspelled words and provides weighted candidate suggestions.

@author: Johannes H. Jensen <joh@pseudoberries.com>
'''

if __name__ == '__main__':
    
    running = True
    while running:
        try:
            s = raw_input()
            
            from spellcheck import Spellcheck
            sc = Spellcheck(s)
            results = sc.results()
            for r in results:
                print r
            
        except (EOFError, KeyboardInterrupt):
            running = False
        
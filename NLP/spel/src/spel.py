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
            for sid in results:
                print 'In sentence "%s":' % (sc.sents[sid])
                for r in results[sid]:
                    print '\t%s: %s' % (r.word, ' '.join(r.candidates))
            
        except (EOFError, KeyboardInterrupt):
            running = False
        
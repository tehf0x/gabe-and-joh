#!/usr/bin/env python
"""
The Spel spellchecker

Spel reads sentences from standard input and prints a list
of misspelled words and provides weighted candidate suggestions.

Useful for testing the spellchecker.

@author: Johannes H. Jensen <joh@pseudoberries.com>
"""

if __name__ == '__main__':
    # Import and create spellchecker
    from spellcheck import Spellchecker
    
    spellchecker = Spellchecker()
    
    lines = []
    while True:
        try:
            lines.append(raw_input())
        except EOFError:
            break
    
    text = ' '.join(lines)
    
    
    results = spellchecker.check(text)
    for r in results:
        print r.word + ':', ' '.join(r.candidates[:5])
    
    print
    print results.corrected()
    print 'Corrected text:'
    
    words = []
    i = 0
    for sent in results.corrected():
        for word in sent:
            # Improve this?
            if i > 0 and not word.isalpha():
                words[i-1] = words[i-1] + word
            else:
                words.append(word)
                i += 1
    
    print ' '.join(words)
    
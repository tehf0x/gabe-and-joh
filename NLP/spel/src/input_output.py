'''
InputParser

Parses test files (XML), and extracts the test cases.
Created on Sep 8, 2009

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''

import xml.dom.minidom
from collections import deque
class InputParser():
    
    def __init__(self, test_xml):
        self.dom_tree =  xml.dom.minidom.parseString(test_xml)
        self.cases = self.dom_tree.getElementsByTagName('case')
    
    
    def get_cases(self):
        for case in self.cases:
            yield {'id' : case.getAttribute('id'), 'string' : case.childNodes[0].data}

class OutputGenerator(deque):
    
    def __init__(self, output_file):
        self.fh = open(output_file, 'w')
        
    def write(self):
        for case in self:
            if not case[2]:
                output = "Case %s, No Misspelled words.\n" % (case[0])
                self.fh.write(output)
                continue
            for c in case[2]:
                candidates =  ', '.join(c.candidates[:5])
                output = "Case %s, %s, %s\n" % (case[0], c.word, candidates)
                self.fh.write(output)
            
'''
TestsParser

Parses test files (XML), and extracts the test cases.
Created on Sep 8, 2009

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''

import xml.dom.minidom

class TestParser():
    
    def __init__(self, test_xml):
        self.dom_tree =  xml.dom.minidom.parseString(test_xml)
        self.cases = self.dom_tree.getElementsByTagName('case')
    
    
    def get_cases(self):
        for case in self.cases:
            yield {'id' : case.getAttribute('id'), 'string' : case.childNodes[0].data}

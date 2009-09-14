#!/usr/bin/python
'''
Created on Sep 14, 2009

Main script for running the spell checker.
@author: Gabe Arnold <gabe@squirrelsoup.net>
'''

from sys import argv
from spellcheck import Spellchecker
from input_output import InputParser, OutputGenerator

if __name__ == '__main__':
    xml_file = argv[1]
    output_name = argv[2]
    
    fh = open(xml_file, 'r')
    input = InputParser(fh.read())
    output = OutputGenerator(output_name)
    
    checker = Spellchecker()
    
    for case in input.get_cases():
        corrections = checker.check(case['string'])
        output.append((case['id'], case['string'], corrections))

    output.write()

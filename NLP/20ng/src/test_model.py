'''
Created on 7 Nov 2009

@author: joh
'''

from model import *

text = 'how are you how are they are bats big rats'

print 'TEXT:', text

m = SLINgramModel(3, text.split())

m.weight = 0.5
m._backoff.weight = 0.3
m._backoff._backoff.weight = 0.2

print m.prob('you', ('how', 'are'))

print m.prob('are', ('','how'))

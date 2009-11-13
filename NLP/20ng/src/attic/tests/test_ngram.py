'''
Created on 7 Nov 2009

@author: joh
'''

from nltk.model import NgramModel
from nltk.probability import LidstoneProbDist

text = 'hi how are you do you like fudge you like cookies'

model = NgramModel(3, text.split(), LidstoneProbDist)



print model.prob('you', ('how','are'))

print model.prob('you', ('how','do'))

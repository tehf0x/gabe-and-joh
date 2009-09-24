'''
Created on Sep 24, 2009

@author: Gabe Arnold
'''

from params import probs, states, H

class TestParams():
    
    
    def test_probs(self):
        for state in states():
            print state
            p = probs(state)
            s = sum(p.values())
            assert sum(p.values()) - 1 <= 1e-10, sum(p.values())
            assert all(sum(v)<=H for v in p.keys())

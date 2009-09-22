"""
Useful assertions

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
"""

import params

def is_state(s):
    return len(s) == len(params.r) == len(params.c) and \
           is_positive(s) and \
           (sum(s) <= params.H)

def is_positive(l):
    return all(e >= 0 for e in l)


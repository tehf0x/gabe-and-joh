"""
Basic parameter calculations

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
"""

from assertions import *


""" Maximum size of the herd """
H = 12

""" Expected utility for young, breedable and old cows respectively """
r = (0.3, 0.4, 0.2)

""" Expected payoff for young, breedable and old cows respectively """
c = (2, 6, 4)



def reward(s, a):
    """ Calculate the reward of doing action a in state s """
    
    # Some sanity checks
    assert is_state(s) and is_state(a)
    assert is_state(tuple(s[i] - a[i] for i in range(len(s))))
    
    return sum([(s[i] - a[i]) * r[i] + a[i] * c[i] for i in range(len(s))])

def prob(s, sp, a):
    """ Calculate the probability from state s to sa when doing action a """
    # TODO: Write Me!
    return 1

def actions(s):
    """ Get all possible actions from state s
    
    A valid action from s is a tuple (y, b, o) for how many young, breedable
    and old cows to sell, respectively. The number of cows to sell cannot
    exceed the number of cows in the given category of the state s.  
    """
    assert is_state(s)
    
    actions = []
    
    for y in range(s[0] + 1):
        for b in range(s[1] + 1):
            for o in range(s[2] + 1):
                actions.append((y, b, o))
    
    return actions
                

def states():
    """ Get all possible states
    
    A valid state is a tuple (y, b, o) for how many young, breedable
    and old cows are in the herd, respectively. The total number of cows
    can not exceed the limit of H cows.
    """
    states = []
    
    for y in range(H + 1):
        for b in range(H - y + 1):
            for o in range(H - y - b + 1):
                states.append((y, b, o))
    
    return states


def afterstate(s, a):
    """ Get the afterstate of state s after doing action a """
    assert is_state(s) and is_state(a)
    
    sa = tuple(s[i] - a[i] for i in range(len(s)))
    
    assert is_state(sa)
    
    return sa




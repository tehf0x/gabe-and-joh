"""
Basic parameter calculations

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
"""

""" Maximum size of the herd """
H = 12

""" Expected utility for young, breedable and old cows respectively """
r = (0.3, 0.4, 0.2)

""" Expected payoff for young, breedable and old cows respectively """
c = (2, 6, 4)


def reward(s, a):
    """ Calculate the reward of doing action a in state s """
    
    # Some sanity checks
    assert len(s) == len(a) == len(r) == len(c),        "Invalid state or action size"
    assert all(e >= 0 for e in s + a),                  "State or action element is negative"
    assert all(s[i]-a[i] >= 0 for i in range(len(s))),  "Action results in negative number of cows"
    assert sum(s) <= H,                                 "Herd size too big (H=%d) " % (H)
    
    return sum([(s[i] - a[i]) * r[i] + a[i] * c[i] for i in range(len(s))])

def prob(s, sn, a):
    """ Calculate the probability from state s to sa when doing action a """
    # TODO: Write Me!
    return 1

def actions(s):
    """ Generate all possible actions from state s
    
    A valid action from s is a tuple (y, b, o) for how many young, breedable
    and old cows to sell, respectively. The number of cows to sell cannot
    exceed the number of cows in the given category of the state s.  
    """
    assert len(s) is 3
    
    for y in range(s[0] + 1):
        for b in range(s[1] + 1):
            for o in range(s[2] + 1):
                yield (y, b, o)
                

def possible_states():
    """ Generate all possible states
    
    A valid state is a tuple (y, b, o) for how many young, breedable
    and old cows are in the herd, respectively. The total number of cows
    can not exceed the limit of H cows.
    """
    for y in range(H + 1):
        for b in range(H - y + 1):
            for o in range(H - y - b + 1):
                yield (y, b, o)



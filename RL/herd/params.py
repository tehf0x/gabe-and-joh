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
"""
Value iteration

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
"""

from params import states, actions, prob, reward, afterstate

def value_iterate(states = states(), actions_fn = actions,
                  prob_fn = prob, reward_fn = reward, 
                  gamma = 0.9, limit = (0.5, None)):
    """ Do value iteration """
    
    theta, sweeps = limit
    
    # Initialize value function to 0
    V = dict((s, 0) for s in states)
    
    assert set(V.keys()) == set(states)
    
    for s in states:
        v = V[s]
        
        #ma = 0
        
        #for a in actions_fn(s):
        #    sp = afterstate(s, a)
        #    print s, a, sp
        #    print prob_fn(s, sp, a) * (reward_fn(s, a) + gamma * V[sp])
            
        
        V[s] = max(prob_fn(s, afterstate(s, a), a) * (reward_fn(s, a) + gamma * V[afterstate(s, a)]) \
                   for a in actions_fn(s))
        
    return V
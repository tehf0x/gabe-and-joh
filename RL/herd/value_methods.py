"""
Value based methods

Heavily dependent on the params module - not generalized whatsoever

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
"""

from params import states, actions, probs, reward, afterstate, H
import sys


def max_action(state, V, gamma = 0.9, debug = False):
    """ Compute the best (action, value) pair from a state 
    
    Returns a tuple: (action, value)
    """
    a_max = None
    v_max = 0
    
    # Loop through all possible actions to determine max value
    for a in actions(state):
        # Choose action a and reach afterstate sa
        sa = afterstate(state, a)
        
        # Milk cows for reward
        r = reward(state, a)
        
        # Go through every possible transition and breeding from afterstate
        sps = probs(sa)
        for sp, p in sps.items():
            vn = p * (r + gamma * V[sp])
            
            if debug:
                print "\n s=%s a=%s sa=%s r=%f sp=%s p=%f V[sp]=%f => vn=%f vs v_max=%f" % \
                        (state, a, sa, r, sp, p, V[sp], vn, v_max)
            
            if vn > v_max:
                v_max = vn
                a_max = a
    
    return (a_max, v_max)



def value_iteration(gamma = 0.9, limit = (0.5, None)):
    """ Value iteration algorithm
    
    gamma -- discount factor
    limit -- specifies when the algorithm should stop (theta, sweeps)
    
    Returns a dictionary V[s] = value 
    """
    
    theta, sweeps = limit
    
    # Initialize value function to 0
    V = dict((s, 0) for s in states())
    
    sweep = 0
    while True:
        sweep += 1
        delta = 0
        
        # Report progress!
        print 'Sweep', sweep, '...',
        sys.stdout.flush()
        
        # Loop through every possible state
        for s in states():
            # Store old value of state
            v = V[s]
            
            an, vn = max_action(s, V, gamma)
            V[s] = vn
            
            delta = max(delta, abs(v - V[s]))
        
        print 'delta =', delta
        
        #raw_input('Hit enter to continue')
        
        if theta and delta < theta:
            break
        
        if sweeps and sweep == sweeps:
            break
        
    return V

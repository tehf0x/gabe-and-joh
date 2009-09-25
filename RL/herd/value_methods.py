"""
Value based methods

Heavily dependent on the params module - not generalized whatsoever

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
"""

from params import states, actions, probs, reward, afterstate, H
import sys

def value(s, r, V, gamma = 0.9):
    """ Calculate the expected value of state s given reward r,
    value function V and discount factor gamma
    """
    v = 0
    sps = probs(s)
    for sp, p in sps.items():
        v += p * (r + gamma * V[sp])
    return v

def max_action(state, V, gamma = 0.9, debug = False):
    """ Compute the best (action, value) pair from a state 
    
    Returns a tuple: (action, value)
    """
    a_max = (0, 0, 0)
    v_max = 0
    
    # Loop through all possible actions to determine max value
    for a in actions(state):
        # Choose action a and reach afterstate sa
        sa = afterstate(state, a)
        
        # Milk cows for reward
        r = reward(state, a)
        
        # Calculate the value of afterstate
        vn = value(sa, r, V, gamma)
        
        if vn > v_max:
            v_max = vn
            a_max = a
    
    return (a_max, v_max)



def value_iteration(gamma = 0.9, theta = 0.01, sweeps = None):
    """ Value iteration algorithm
    
    gamma -- discount factor
    theta -- stop when delta < theta
    sweeps -- stop after N sweeps
    
    Returns a dictionary V[s] = value 
    """
    
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
            
            # Update delta
            delta = max(delta, abs(v - V[s]))
        
        print 'delta =', delta
        
        #raw_input('Hit enter to continue')
        
        if theta and delta < theta:
            break
        
        if sweeps and sweep == sweeps:
            break
        
    return V


def policy_iteration(gamma = 0.9, theta = 0.01, sweeps = None):
    """ Policy iteration
    
    gamma -- discount factor
    theta -- stop when delta < theta
    sweeps -- stop after N sweeps
    
    Returns a tuple (pi*, V*) where
        pi*[s] = action
        V*[s] = value
    """
    
    theta, sweeps = limit
    
    # Initialize value function to 0
    V = dict((s, 0) for s in states())
    
    # Initialize value function to 0
    V = dict((s, 0) for s in states())
    
    # Initialize policy to (0, 0, 0)
    pi = dict((s, (0, 0, 0)) for s in states())
    
    # Assume a stable policy
    policy_stable = False
    
    while not policy_stable:
        # 
        # Policy Evaluation
        #
        print "Policy Evaluation..."
        sweep = 0
        while True:
            sweep += 1
            delta = 0
            
            # Report progress!
            print '\tSweep', sweep, '...',
            sys.stdout.flush()
            
            # Loop through every possible state
            for s in states():
                # Store old value of state
                v = V[s]
                
                # Act according to policy
                sa = afterstate(s, pi[s])
                V[s] = value(sa, reward(s, pi[s]), V, gamma)
                
                # Update delta
                delta = max(delta, abs(v - V[s]))
            
            print 'delta =', delta
            
            #raw_input('Hit enter to continue')
            
            if theta and delta < theta:
                break
            
            if sweeps and sweep == sweeps:
                break
        
        
        #
        # Policy Improvement
        #
        print "Policy Improvement..."
        
        policy_stable = True
        
        # Go through every state
        for s in states():
            b = pi[s]
            
            an, vn = max_action(s, V, gamma)
            pi[s] = an
            
            #print "pi[%s] = %s" % (s, pi[s])
            
            if b != pi[s]:
                policy_stable = False
        
        
    # Return the value function and policy
    return V, pi
    
    
    
    
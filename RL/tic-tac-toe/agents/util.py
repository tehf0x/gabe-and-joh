"""
Tic-Tac-Toe utility functions
"""

def pos_str(pos):
    """ Convert numerical board positions to strings """
    values = ['_', 'x', 'o']
    if isinstance(pos, list):
        return ' '.join([pos_str(i) for i in pos])
    else:
        return values[pos]

def state_str(states, delimiter="  =>  "):
    """ Pretty board string representation. 
    If a list of states is provided, they will be placed horizontally
    with {delimiter} as a separator. """
    
    if not isinstance(states[0], list):
        states = [states]
    
    dlen = len(delimiter)
    
    s = ""
    for i in 0, 3, 6:
        d = " " * dlen
        if i is 3:
            d = delimiter
        
        s += d.join([pos_str(s[i:i+3]) for s in states]) + "\n"
    
    return s

def print_state(states, delimiter="  =>  "):
    """ Pretty-print board states. See state_str() """
    print state_str(states, delimiter)
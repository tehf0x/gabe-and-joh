"""


"""

t_probs = ((0.9, 0.1, 0),
           (0, 0.75, 0.25),
           (0, 0.15, 0.85))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = value = self.func(*args)
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
        
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

def hash_13(state):
    return state[0] * 13**2 + state[1] * 13 + state[2]

def join_states(states):
    cows = []
    probs = []
    #Split up into the states and the corresponding probabilities.
    for state in states:
        cows.append(state[0])
        probs.append(state[1])
    return (sum_tuples(cows), prod_probs(probs))
    
def prod_probs(probs):
    val = 1
    for prob in probs:
        val *= prob
    return val

def sum_tuples(tuples):
    '''
    Take the tuples and sum them as if they were matrices.
    '''
    new_tuple = [0,] * len(tuples[0])
    for l in tuples:
        for t in range(len(l)):
            new_tuple[t] += l[t]
    return tuple(new_tuple)

#Inspired by http://automatthias.wordpress.com/2007/04/28/cartesian-product-of-multiple-sets/   
def cartesian_product(lists):
    if(len(lists) == 1):
        for el in lists[0]:
            yield (el,)
    else:
        for el in lists[0]:
            for x in cartesian_product(lists[1:]):
                yield (el,) + x
    
@memoized
def calc_prob(post_state):
    print 'not cached'
    ret_states = {}
    s_prime= set()
    sub_states = [0]*len(post_state)
    '''
    For each element in the post state, figure out all ways it can be spread out.
    Example for (5,4,3):
    So figure out all the ways (5,0,0) can be spread out (4,1,0),(4,0,1),(3,2,0)...
    along with the probability of each new sub-state happening.
    Then recombine all the sub-states together to have every possible resulting
    state, and calculate the resulting probability of each distinct new state. 
    '''
    for pos in range(len(post_state)):
        sub_states[pos] = set()
        el = post_state[pos]
        print el
        if el == 0:
            sub_states[pos].add(((0,0,0), 1))
            continue
        '''
        Figure out all attainable states and their likelihood.
        I'm iterating through every possible state, and only saving those with
        the right total number of cows.
        A bit of base 13 trickery going on here, replace 13 by 10 and it'll make
        sense
        '''
        for i in range(2197):
            s = (i/(13**2), (i/13)%13, i%13)
            #Keep a state if has the same number of cows as the original state
            if(sum(s) == el):
                p = t_probs[pos]
                #Calculate the probability of this state happening
                prob = (p[0]**s[0])*(p[1]**s[1])*(p[2]**s[2])
                #If it's possible, save it
                if(prob > 0):
                    sub_states[pos].add((s, prob))
    #Now for combine all the sub_states together in every possible way
    print sub_states
    for states in cartesian_product(sub_states):
        print states
    new_states = [join_states(states) for states in cartesian_product(sub_states)]
    for state in new_states:
        try:
            ret_states[state[0]] += state[1]
        except KeyError,e:
            ret_states[state[0]] = state[1]
    return ret_states
    
if __name__ == '__main__':
    probs = calc_prob((2,2,2))
    yp = 0
    for x,y in probs.items():
        yp += y
        print x, y
    print yp

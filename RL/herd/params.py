"""
Basic parameter calculations

@author: Johannes H. Jensen <johannj@stud.ntnu.no>
@author: Gabe Arnold <gabe@squirrelsoup.net>
"""

from assertions import *
from gmpy import comb

""" Maximum size of the herd """
H = 12

""" Expected utility for young, breedable and old cows respectively """
r = (0.3, 0.4, 0.2)

""" Expected payoff for young, breedable and old cows respectively """
c = (2, 6, 4)

'''Transition probabilities from one type of cow to another.'''
t_probs = ((0.9, 0.1, 0),
           (0, 0.75, 0.25),
           (0, 0.15, 0.85))


'''Birth probabilities for breedable cows.'''
birth_prob = (0.050, 0.80, 0.150)


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

def concat_multiples(states):
    '''
    Takes elements in the list that are the same, and sums their probabilities
    into a single entry.  Each element of the list must be of the form
    (element, probability).
    Return a dictionary where the keys are the elements, and their values 
    are the probabilities.
    '''
    concat_dict = {}
    for state in states:
        try:
            concat_dict[state[0]] += state[1]
        except KeyError,e:
            concat_dict[state[0]] = state[1]
    return concat_dict
    

def join_states(states):
    '''
    Adds state together, summing the states  and multiplying probabilities.
    '''
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
def breed(cows, offspring = [(0,1)]):
    '''
    Recursive function that finds out the probabilities for the 
    resulting number of offspring from breeding 'cows' cows.
    Do not pass 'offspring' parameter, just cows = #breedable cows
    '''
    if cows == 0:
        concat_children = {}
        for children in offspring:
            try:
                concat_children[children[0]] += children[1]
            except KeyError, e:
                concat_children[children[0]] = children[1]
        return concat_children
    
    old_offspring = offspring[:]
    offspring = []
    for off in old_offspring:
        offspring.append((off[0], off[1] * birth_prob[0]))
        offspring.append((off[0] + 1, off[1] * birth_prob[1]))
        offspring.append((off[0] + 2, off[1] * birth_prob[2]))
    return breed(cows-1, offspring)

              
@memoized
def probs(post_state):
    """ Get all possible sub-states from post_state and their probabilities """

#    print 'not cached'
    
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
        for s in states():
            if(sum(s) == el):
                p = t_probs[pos]
                #Calculate the probability of this state happening
                prob = (p[0]**s[0])*(p[1]**s[1])*(p[2]**s[2])
                #Correct the probability for states that can occur multiple ways
                prob *= comb(el, max(s)) #Uses combinations
                #If it's possible, save it
                if(prob > 0):
                    sub_states[pos].add((s, prob))
    #Now for combine all the sub_states together in every possible way
    new_states = [join_states(j_states) for j_states in cartesian_product(sub_states)]
    prebirth = concat_multiples(new_states)
    #Now calculate birth probabilities:
    postbirth = list()
    for state in new_states:
        #This returns all the different amounts of cows that can be produced, along with probability.
        offspring = breed(state[0][1])
        for off in offspring:
            if sum(state[0]) + off > H:
                calves = H - sum(state[0])
                num_young = state[0][0] + calves
            else:
                num_young = state[0][0] + off
            postbirth.append(((num_young, state[0][1], state[0][2]), 
                              state[1] * offspring[off]))

    ret_states = concat_multiples(postbirth)
    return ret_states

def reward(s, a):
    """ Calculate the reward of doing action a in state s """
    
    # Some sanity checks
    assert is_state(s) and is_state(a)
    assert is_state(tuple(s[i] - a[i] for i in range(len(s))))
    
    return sum([(s[i] - a[i]) * r[i] + a[i] * c[i] for i in range(len(s))])

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

        
if __name__ == '__main__': 
    for state in states():
            print state
            p = probs(state)
            s = sum(p.values())
            assert sum(p.values()) - 1 <= 1e-10, sum(p.values())
            assert all(sum(v)<=H for v in p.keys())
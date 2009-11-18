'''
Fancy-shmancy tiling class.

Gabe
'''

import random
from copy import copy
from collections import defaultdict

class CmacTiler:

    def __init__(self, size, densities):
        '''
        size is a (width, height) tuple of the actual gridworld
        n_tilings is the number of different tilings we want to use
        '''
        self.tilings = []
        self.action_set = ActionSet(self)
        self.size = size
        for dens in densities:
            self.tilings.append(Tiling(size, dens))
        self.n_tilings = float(len(self.tilings))


    def __getitem__(self, pos):
        tiler_actions = []
        for tiling in self.tilings:
            tiler_actions.append(tiling[pos])
        
        return ActionSet(tiler_actions)


class Tiling:
    '''
    Contains a reduction map as well as a value store.
    '''
    actions = [('E',), ('N',), ('S',), ('W',)]
    #actions = {('E',): 0, ('N',): 0, ('S',): 0, ('W',): 0}

    def __init__(self, size, dens):
        '''
        Generate the tilings for a density 'dens'.
        '''
        #We do dens-1 because we need 9 walls split a space into 10 cells.
        self.x_map = random.sample(xrange(size[0]), dens-1)
        self.y_map = random.sample(xrange(size[1]), dens-1)
        self.x_map.sort()
        self.y_map.sort()
        self.values = defaultdict(lambda: None)

    def map_val(self, map, coord):
        '''Map a coordinate to its tiling.'''
        #As soon as the coord is smaller than the index, then we have
        #hit the upper limit of that tile.
        for idx, val in enumerate(map):
            if val >= coord:
                return idx

        #Or if we're in the last tile:
        return len(map)

    def __getitem__(self, pos):
        '''
        Return the dict of actions for the requested state.
        This *has* to return the proper reference to the dict, so that
        when someone does tile[pos][action] = 5 it gets properl updated.
        '''
        mapped_x = self.map_val(self.x_map, pos[0])
        mapped_y = self.map_val(self.y_map, pos[1])

        #To avoid that we look it up twice every time to check if it's none
        #look up the value once, and if it's not inited, init it.
        val = self.values[(mapped_x, mapped_y)]
        if val is None:
            self.values[(mapped_x, mapped_y)] = self.random_actions()
            
            #self.values[(mapped_x, mapped_y)] = copy(self.actions)
            #Need to copy it back to keep the references correct.
            val = self.values[(mapped_x, mapped_y)]

        return val
    
    random.random()
    
    def random_actions(self):
        """ Generate random action values """
        return dict((a, random.random()) for a in self.actions)

class ActionSet:
    '''
    This exists as a wrapper to the array of actions.
    When an action value gets updated by the RL agent, the actionset
    calls the cmactiler's update functino with the new value so that
    it gets properly distributed over the different tilings.
    '''
    def  __init__(self, tiler_actions):
        self.tiler_actions = tiler_actions
    
    def __getitem__(self, action):
        '''
        Calculate the average of one action over the different tilers.
        We will *not* do this:
        dict((k, float(sum([e[k] for e in d]))/len(d)) for k in d1.keys())
        '''
        avg_action = float(sum([actions[action] for actions in self.tiler_actions])) \
                     / len(self.tiler_actions)
                     
        return avg_action
    
    def __setitem__(self, action, value):
        ''' Sets the value of action for all tilers '''
        for tiler_action in self.tiler_actions:
            tiler_action[action] = value
    
    def __repr__(self):
        return str(dict(self.items()))
    
    def keys(self):
        return self.tiler_actions[0].keys()
    
    def items(self):
        return [(k, self[k]) for k in self.keys()]
    
    def values(self):
        return [self[k] for k in self.keys()]




"""
MENACE agent

< Some description here >

Authors:
    Johannes H. Jensen <johannj@stud.ntnu.no>
    Gabe Dulac-Arnold <gabe@squirrelsoup.net>

Agent settings can be modified real-time by sending messages to the
agent through RL-Glue. The format is <setting>=<value>
"""

import sys
import copy
import re
import random

from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.types import Observation


class Matchbox:
    """ Matchbox class representing a matchbox for a state containing N marbles
    of each color for every possible subsequent state """
    
    # Whether to enable negative rewards, i.e. if we should remove
    # marbles in pick_marble()
    remove_marbles = True
    
    def __init__(self, state, marble_count, remove_marbles=True):
        """ Create a matchbox for state with marble_count marbles per subsequent state """
        self.state = state
        self.marbles = []
        self.remove_marbles = remove_marbles
        
        # Place initial marbles in the matchbox
        for color in range(state.count(0)):
            self.marbles.extend([color for i in range(marble_count)])
    
    def pick_marble(self):
        """ Pick a random marble from matchbox """
        if self.marbles:
           i = random.randint(0, len(self.marbles) - 1)
           marble = self.marbles[i]
            
           if self.remove_marbles:
               self.marbles.remove(marble)
                
        else:
            # There are no marbles left in the box, so we choose a random one
            print "Matchbox: No marbles left! Choosing random..."
            marble = random.randint(0, self.state.count(0) - 1)
        
        return marble
    
    def put_marbles(self, color, count=1):
        """ Place 'count' marbles of a color in matchbox """
        self.marbles.extend([color for i in range(count)])
    
    def __str__(self):
        return 'Matchbox state: %s with marbles: %s' % (self.state, self.marbles)


def pos_str(pos):
    """ Convert numerical board positions to strings """
    values = ['_', 'x', 'o']
    if isinstance(pos, list):
        return ' '.join([pos_str(i) for i in pos])
    else:
        return values[pos]

def state_str(state):
    """ Pretty board string representation """
    s = ""
    for row in range(3):
        for col in range(3):
            v = int(state[3*row + col])
            if v is 1:
                s += 'x'
            elif v is 2:
                s += 'o'
            else:
                s += ' '
            
            s += " "
        s += "\n"
    
    return s

def state_print(state):
    """ Pretty-print a board state """
    for i in 0, 3, 6:
        print pos_str(state[i,i+3])


class MenaceAgent(Agent):
    """
    The MENACE agent class
    """
    
    """ Initial marble count """
    marble_count = 4
    
    """ Marble increment for each step """
    marble_inc = -1
    
    """ Marble win reward, i.e. number of marbles to place back into the matchboxes
    that resulted in a positive reward """
    marble_win_reward = 3
    
    """ Whether to remove marbles from matchboxes """
    marble_remove = True
    
    """ Matchbox collection """
    matchboxes = {}
    
    """ List of moves we've done so far - each element is a tuple (marble, matchbox) """
    moves = []
    
    
    def agent_init(self, taskSpec):
        pass
    
    def state_hash(self, state):
        """ Create a unique hash for a state """
        return ''.join([str(i) for i in state])
    
    def get_matchbox(self, state):
        """ Get matchbox for a state. Dynamically creates unseen states. """
        hash = self.state_hash(state)
        if self.matchboxes.has_key(hash):
            return self.matchboxes[hash]
        else:
            # Determine which step we're taking, 0, 1, 2 or 3
            step = int(4 - (state.count(0) - 1) / 2)
            count = self.marble_count + self.marble_inc * step
            matchbox = Matchbox(state, count, self.marble_remove)
            self.matchboxes[hash] = matchbox
            return matchbox
    
    def play(self, matchbox):
        """ Play from matchbox, returns a tuple of (marble, new_state) """
        state = copy.copy(matchbox.state)
        
        # Determine which actions we can take
        actions = []
        for i in range(len(state)):
            if state[i] == 0:
                actions.append(i)
        
        # Pick a random marble from matchbox
        marble = matchbox.pick_marble()
        
        # Choose the corresponding action
        state[actions[marble]] = 1
        
        return (marble, state)
    
    
    def do_step(self, state):
        """ Do an agent step """
        state = list(state)
        
        # Only keep matchboxes for non-terminal states
        if state.count(0) > 1:
            # Get the matchbox for this state
            matchbox = self.get_matchbox(state)
            
            # Play
            marble, new_state = self.play(matchbox)
            
            # Store this move for learning
            self.moves.append((marble, matchbox))
        else:
            # Only one option left, play it but don't learn
            new_state = copy.copy(state)
            i = state.index(0)
            new_state[i] = 1
        
        # Some debugging output
        for i in 0, 3, 6:
            d = "    "
            if i is 3:
                d = " => "
            
            print pos_str(state[i:i+3]), d, pos_str(new_state[i:i+3])
        
        print
        
        # Return new state to environment
        action = Action()
        action.intArray = new_state
        
        return action
    
    def agent_start(self, state):
        """ Called every time a new game is started """
        print "GAME START!"
        self.moves = []
        return self.do_step(state.intArray)
    
    def agent_step(self, reward, state):
        """ Called for each game step """
        return self.do_step(state.intArray)
    
    def print_moves(self):
        marbles = [("(%d)" % (m[0])).center(5) for m in self.moves]
        print "      ".join(marbles)
        
        for i in 0, 3, 6:
            d = "      "
            if i is 3:
                d = "  =>  "
            
            print d.join([pos_str(m[1].state[i:i+3]) for m in self.moves])
    
    def agent_end(self, reward):
        """ Called when a game ends, this is where we learn """
        print "GAME END, REWARD: ", str(reward)
        print "*************************************************"
        self.print_moves()
        print "\n*************************************************\n"
        
        if reward:
            # We won, reward matchboxes
            for color, matchbox in self.moves:
                matchbox.put_marbles(color, self.marble_win_reward)
    
    def agent_cleanup(self):
        """ Clean up for next run """
        self.matchboxes = {}
        self.moves = []
    
    def agent_message(self, msg):
        """ Retrieve message from the environment in the form param=value """
        result = re.match('(.+)=(.+)', msg)
        if result:
            param, value = result.groups()
            if param == 'marble_inc':
                self.marble_inc = int(value)
            elif param == 'marble_count':
                self.marble_count = int(value)
            elif param == 'marble_win_reward':
                self.marble_win_reward = int(value)
            elif param == 'marble_remove':
                self.marble_remove = bool(value)
            else:
                return "Unknown parameter: " + param
            
        else:
            return "Unknown command: " + msg;


if __name__=="__main__":
    AgentLoader.loadAgent(MenaceAgent())
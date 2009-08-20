# 
# Base MENACE agent
#

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
    
    def __init__(self, state, marble_count):
        """ Create a matchbox for state with marble_count marbles per subsequent state """
        self.state = state
        self.marbles = []
        
        # Place initial marbles in the matchbox
        for color in range(state.count(0)):
            self.marbles.extend([color for i in range(marble_count)])
    
    def pick_marble(self):
        """ Pick a random marble from matchbox """
        i = random.randint(0, len(self.marbles) - 1)
        marble = self.marbles[i]
        self.marbles.remove(marble)
        
        return marble
    
    def put_marbles(self, color, count=1):
        """ Place count marbles of color in matchbox """
        self.marbles.extend([color for i in range(count)])
    
    def __str__(self):
        return 'Matchbox state: %s with marbles: %s' % (self.state, self.marbles)

def state_str(state):
    s = ""
    for row in range(3):
        for col in range(3):
            s += str(state[3*row + col]) + " "
        s += "\n"
    
    return s

def state_print(state):
    """ Pretty-print a board state """
    print state_str(state)
'''    for row in range(3):
        for col in range(3):
            print state[3*row + col],
        print
'''

class MenaceAgent(Agent):
    """ Initial marble count """
    marble_count = 4
    
    """ Marble increment for each step """
    marble_inc = -1
    
    """ Marble win reward, i.e. number of marbles to place back into the matchboxes
    that resulted in a positive reward """
    marble_win_reward = 3
    
    """ Matchbox collection """
    matchboxes = {}
    
    """ List of moves we've done so far - each element is a tuple (marble, matchbox) """
    moves = []
    
    def agent_init(self, taskSpec):
        print "agent_init()"
    
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
            matchbox = Matchbox(state, count)
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
        
        print "play marble #%d: " % (marble)
        state_print(state)
        
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
            
            # Get matchbox for next state and store this move
            #new_matchbox = self.get_matchbox(new_state)
            self.moves.append((marble, matchbox))
        else:
            # Only one option left, play it
            new_state = copy.copy(state)
            i = state.index(0)
            new_state[i] = 1
            
            print "play #%d: " % (i)
            state_print(new_state)
        
        # Return new state to environment
        action = Action()
        action.intArray = new_state
        return action
    
    def agent_start(self, state):
        print "agent_start(", state.intArray, ")"
        self.moves = []
        return self.do_step(state.intArray)
    
    def agent_step(self, reward, state):
        print "agent_step(", reward, ",", state.intArray, ")"
        return self.do_step(state.intArray)
    
    def agent_end(self, reward):
        print "agent_end(", str(reward), ")"
        
        if reward:
            print "We won! Reward matchboxes..."
            for color, matchbox in self.moves:
                matchbox.put_marbles(color, self.marble_win_reward)
                print "\t#", color, ":", matchbox.state, "+", self.marble_win_reward, "of color", color, "=", matchbox.marbles.count(color), "total"
    
    def agent_cleanup(self):
        print "agent_cleanup()"
    
    def agent_message(self, msg):
        """ Retrieve message from the environment in the form param=value """
        print "agent_message(", msg, ")"
        
        result = re.match('(.+)=(.+)', msg)
        if result:
            param, value = result.groups()
            if param == 'marble_inc':
                self.marble_inc = int(value)
            elif param == 'marble_count':
                self.marble_count = int(value)
            else:
                return "Unknown parameter: " + param
            
        elif msg == 'show matchboxes':
            ret = ''
            for k in self.matchboxes:
                m = self.matchboxes[k]
                ret += state_str(m.state)
                ret += str(m.marbles)
                ret += "\n"
            
            return ret
            
        else:
            return "Unknown command: " + msg;


if __name__=="__main__":
    AgentLoader.loadAgent(MenaceAgent())
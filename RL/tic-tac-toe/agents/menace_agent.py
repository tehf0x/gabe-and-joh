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
import pickle

from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.types import Observation

from util import print_state


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

class MenaceAgent(Agent):
    """
    The MENACE agent class
    """
    
    """ Which player are we? 1 or 2 """
    player = 1
    
    """ Initial marble count """
    marble_count = 4
    
    """ Marble increment for each step """
    marble_inc = -1
    
    """ Marble win reward, i.e. number of marbles to place back into the matchboxes
    that resulted in a positive reward """
    marble_win_reward = 3
    
    """ Marble win reward increment. Will be applied starting from the first move. """
    marble_win_inc = 0
    
    """ Whether to remove marbles from matchboxes """
    marble_remove = True
    
    """ Set this to a filename to save the learned matchboxes """
    save_to = None
    
    """ Set this to a filename to load learned matchboxes """
    load_from = None
    
    """ Matchbox collection """
    matchboxes = {}
    
    """ List of moves we've done so far - each element is a tuple (marble, matchbox) """
    moves = []
    
    
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
    
    def save_matchboxes(self, filename):
        """ Save matchboxes to file """
        print "SAVING TO", filename
        fh = open(filename, 'w')
        pickle.dump(self.matchboxes, fh)
        fh.close()
    
    def load_matchboxes(self, filename):
        """ Load matchboxes from file """
        print "LOADING FROM", filename
        fh = open(filename, 'r')
        self.matchboxes = pickle.load(fh)
        fh.close()
    
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
        state[actions[marble]] = self.player
        
        return (marble, state)
    
    
    def do_step(self, state):
        """ Do an agent step """
        state = list(state)
        
        # Get the matchbox for this state
        matchbox = self.get_matchbox(state)
        
        # Play
        marble, new_state = self.play(matchbox)
        
        # Store this move for learning
        self.moves.append((marble, matchbox))
        
        # Some debugging output
        print_state([state, new_state])
        print
        
        # Return new state to environment
        action = Action()
        action.intArray = new_state
        
        return action
    
    def print_moves(self):
        """ Print the agent's moves so far """
        marbles = [("(%d)" % (m[0])).center(5) for m in self.moves]
        print "      ".join(marbles)
        
        print_state([m[1].state for m in self.moves])
    
    def learn(self):
        """ Learn from our moves """
        i = 0
        for color, matchbox in self.moves:
            reward = self.marble_win_reward + self.marble_win_inc * i
            matchbox.put_marbles(color, reward)
            print "LEARN: REWARD MOVE #%d with %d of (%d)-marbles" % (i, reward, color)
            i += 1
    
    def agent_init(self, taskSpec):
        pass
    
    def agent_start(self, state):
        """ Called every time a new game is started """
        print "GAME START!"
        self.moves = []
        return self.do_step(state.intArray)
    
    def agent_step(self, reward, state):
        """ Called for each game step """
        return self.do_step(state.intArray)
    
    def agent_end(self, reward):
        """ Called when a game ends, this is where we learn """
        print "GAME END, REWARD: ", str(reward)
        print "*************************************************"
        self.print_moves()
        print "*************************************************\n"
        
        if reward:
            # We won or it was a draw, do some learning!
            self.learn()
                
    def agent_cleanup(self):
        """ Clean up for next run """
        print
        print "RESET AGENT"
        print
        
        if self.save_to:
            # Save matchboxes to file
            self.save_matchboxes(self.save_to)
        
        self.matchboxes = {}
        self.moves = []
        
        if self.load_from:
            # Load matchboxes from file
            self.load_matchboxes(self.load_from)
    
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
            elif param == 'marble_win_inc':
                self.marble_win_inc = int(value)
            elif param == 'marble_remove':
                self.marble_remove = bool(value)
            elif param == 'save_to' and value != 'None':
                self.save_to = str(value)
            elif param == 'load_from' and value != 'None':
                self.load_from = str(value)
            else:
                return "Unknown parameter: " + param
            
        else:
            return "Unknown command: " + msg;


if __name__=="__main__":
    AgentLoader.loadAgent(MenaceAgent())
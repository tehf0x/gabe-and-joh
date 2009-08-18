# 
# Copyright (C) 2008, Brian Tanner
# 
#http://rl-glue-ext.googlecode.com/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import random
import sys
import copy
import re
from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.types import Observation

from random import Random

class Matchbox:
    def __init__(self, state, marble_count):
        self.state = state
        marble_colors = 0
        for i in state:
            if i == 0:
                marble_colors += 1
        
        self.marbles = []
        for color in range(marble_colors):
            self.marbles.extend([color for i in range(marble_count)])
            
    def __str__(self):
        return 'Matchbox state: %s with marbles: %s' % (self.state, self.marbles)

def state_hash(state):
    hash = 0
    r = 0
    for s in state:
        hash += s * (10 ** r)
        r += 1
    
    return hash

state = [0, 1, 2, 0, 0, 1, 0, 0, 2]
print "hash:", state_hash(state)

class menace_agent(Agent):
    """ Initial marble count """
    marble_count = 4
    
    """ Marble increment for each step """
    marble_inc = -1
    
    """ Matchbox collection """
    matchboxes = {}
    
    """ List of moves we've done so far """
    moves = []
    
    randGenerator=Random()
    lastAction=Action()
    lastObservation=Observation()
    
    def agent_init(self,taskSpec):
        #See the sample_sarsa_agent in the mines-sarsa-example project for how to parse the task spec
        self.lastAction=Action()
        self.lastObservation=Observation()
    
    def state_hash(self, state):
        """ Create a unique hash for a state """
        return ''.join([str(i) for i in state])
    
    def get_matchbox(self, state):
        """ Get matchbox for a state. Dynamically creates unseen states. """
        hash = self.state_hash(state)
        if self.matchboxes.has_key(hash):
            return self.matchboxes[hash]
        else:
            matchbox = Matchbox(state, self.marble_count)
            self.matchboxes[hash] = matchbox
    
    def play(self, state):
        """ Play from matchbox, returns next state """
        # Determine which actions we can take
        actions = []
        for i in range(len(state)):
            if state[i] == 0:
                actions.append(i)
        
        # Choose a random action from the possible actions
        a = self.randGenerator.randint(0, len(actions))
        state[actions[a]] = 1
        
        return state
    
    def do_step(self, state):
        # Get the matchbox for this state
        matchbox = self.get_matchbox(state)
        
        # Play
        new_state = self.play(state)
        
        # Store this state for later
        matchbox
        
        # Return new state to environment
        action = Action()
        action.intArray = new_state
        return action
    
    def agent_start(self, state):
        #Generate random action, 0 or 1
        print "start: Got observation: ", observation.intArray
        
        # Get the matchbox for this state
        matchbox = self.get_matchbox(state)
        
        # Play
        new_state = self.play(state)
        
        # Return new state to environment
        action = Action()
        action.intArray = new_state
        return action
    
    def agent_step(self,reward, observation):
        #Generate random action, 0 or 1
        print "step: Got observation: ", observation.intArray
        thisIntAction=self.randGenerator.randint(0,1)
        returnAction=Action()
        returnAction.intArray=[thisIntAction]
        
        lastAction=copy.deepcopy(returnAction)
        lastObservation=copy.deepcopy(observation)

        return returnAction
    
    def agent_end(self,reward):
        pass
    
    def agent_cleanup(self):
        pass
    
    def agent_message(self, msg):
        """ Retrieve message from the environment in the form param=value """
        result = re.match('(.+)=(.+)', msg)
        if result:
            param, value = result.groups()
            if param == 'marble_inc':
                self.marble_inc = int(value)
            elif param == 'marble_count':
                self.marble_count = int(value)
            else:
                return "Unknown parameter: " + param
        else:
            return "Unknown command: " + msg;


if __name__=="__main__":
    AgentLoader.loadAgent(menace_agent())
"""
Temporal Different base agent

See the README for details

Authors:
    Johannes H. Jensen <johannj@stud.ntnu.no>
    Gabe Dulac-Arnold <gabe@squirrelsoup.net>

Agent settings can be modified real-time by sending messages to the
agent through RL-Glue. The format is <setting>=<value>
"""

import re
import random
from copy import copy

from rlglue.agent.Agent import Agent
from rlglue.types import Action
from rlglue.types import Observation

from base import BaseAgent


class TDAgent(BaseAgent):
    """
    Base agent for TD learning.
    """
    # Name of this agent
    name = 'TDAgent'
    
    # The 4 actions we can take.
    # TODO: Should be moved to taskSpec!
    actions = [('E',), ('N',), ('S',), ('W',)]

    # Discount Gamma value
    # TODO: Should be moved to taskSpec
    gamma = 0.9
    
    # Q-Update Alpha Value
    alpha = 0.01
    
    # Epsilon-Greed epsilon value
    epsilon = 0.1
    
    # Epsilon is multiplied by this parameter for each episode
    #epsilon_mul = 0.9993
    epsilon_mul = 1.0
    
    # Initialize Q
    Q = {}

    # We need to remember our last action and state for updating Q
    last_state = ()
    last_action = ()
    
    def agent_init(self, task_spec):
        """Re-initialize the agent for a new training round."""
        self.debug("INIT")
        self.Q = {}

    def agent_start(self, state):
        """ Called every time a new game is started """
        self.debug("START")
        self.epsilon *= self.epsilon_mul
        #print 'epsilon =', self.epsilon
        state = tuple(state.intArray)
        return self.do_step(state)

    def agent_step(self, reward, state):
        """ Called for each game step """
        state = tuple(state.intArray)
        return self.do_step(state, reward)

    def agent_end(self, reward):
        """ Called when a game ends """
        self.debug("END")

    def agent_cleanup(self):
        """ Clean up for next run """
        self.Q = {}
        self.debug("CLEANUP")
    
    def do_step(self, state, reward = None):
        """
        Runs the actual learning algorithm.
        In a separate function so it can be called both on start and on step.
        """
        a_obj = Action()
        
        # Query the policy to find the best action
        action = self.policy(state)
        a_obj.charArray = list(action)
        
        # Run the Q update if this isn't the first step
        if reward is not None:
            self.update_Q(self.last_state, self.last_action, reward, state)
            
        # Save the current state-action pair for the next step's Q update.
        self.last_state = state
        self.last_action = action
        
        # And we're done
        return a_obj

    def update_Q(self, state, action, reward, new_state):
        """
        Update the Q value of this state-action pair.
        This should be implemented in the child class
        """
        raise NotImplementedError

    def random_actions(self):
        """ Generate random action values """
        return dict((a, random.random()) for a in self.actions)
    
    def policy(self, state):
        """
        Return the action to be taken for the state given.
        """
        
        # Determine the best action
        if not state in self.Q:
            # State not yet visited, initialize randomly
            self.Q[state] = self.random_actions()
        
        # Greedily select the best action
        action = max(self.Q[state].items(), key=lambda x : x[1])[0]
        
        # Epsilon-greedy decision:
        if(random.uniform(0, 1) <= self.epsilon):
            # Explore!
            tmp_actions = copy(self.actions)
            tmp_actions.remove(action)
            return random.choice(tmp_actions)
        else:
            # Greediness!
            return action

    def export_policy(self):
        """ Export the policy as a 2 dimensional list of actions. """
        # Back up the epsilon and set it to zero so that we don't export
        # exploring moves in the final deterministic policy.
        bak_epsilon = self.epsilon
        self.epsilon = 0
        
        rows, cols = max(self.Q)
        rows += 1
        cols += 1
        a = [[0]*cols for i in range(rows)]
        for row in range(rows):
            for col in range(cols):
                a[row][col] = self.policy((row, col))
        
        # Set epsilon back to the original
        self.epsilon = bak_epsilon
        
        return a

    
    
    def agent_message_get_param(self, param):
        """ Get a parameter via message """
        if param == 'policy':
            return repr(self.export_policy())
        
        return BaseAgent.agent_message_get_param(self, param)
    
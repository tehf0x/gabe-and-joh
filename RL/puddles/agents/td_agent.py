"""
Q-Learning Agent

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


class TDAgent(Agent):
    """
    Base agent for TD learning.
    """

    #The 4 actions we can take.
    actions = [('E',), ('N',), ('S',), ('W',)]

    #Some constants
    #Discount Gamma value
    gamma = 0.9
    #Q-Update Alpha Value
    alpha = 0.01
    #Epsilon-Greed epsilon value
    epsilon = 0.1
    #Initialize Q
    Q = {}
    #What type of learning is this:
    name = 'TD'

    #We need to remember our last action and state for updating Q
    last_state = []
    last_action = []

    def update_Q(self, state, action, reward, new_state):
        """
        Update the Q value of this state-action pair.
        This should be implemented in the child class
        """
        print "Not Implemented."
        pass

    def policy(self, state):
        """
        Return the action to be taken for the state given.
        """
        #Greedy policy means pick the best action:
        try:
            v = self.Q[state].values()[0]
            if all( i == v for i in self.Q[state].values()):
                #It's *sort of* a value error, right?
                raise ValueError
            action = max(self.Q[state].items(), key=lambda x : x[1])[0]
        except (KeyError, ValueError):
            action = random.choice(self.actions)

        #Epsilon-greedy decision:
        if(random.uniform(0, 1) <= self.epsilon):
            tmp_actions = copy(self.actions)
            tmp_actions.remove(action)
            return random.choice(tmp_actions)
        else:
            return action

    def do_step(self, state, reward = None):
        """
        Runs the actual Q-Learning algorithm.
        In a separate function so it can be called both on start and on step.
        """
        a_obj = Action()
        #Query the policy to find the best action
        action = self.policy(state)
        a_obj.charArray = list(action)
        #Run the Q update if this isn't the first step
        if reward != None:
            self.update_Q(tuple(self.last_state), tuple(self.last_action),
                          reward, tuple(state))
        #Save the current state-action pair for the next step's Q update.
        self.last_state = state
        self.last_action = action
        #And we're done
        return a_obj

    def export_policy(self):
        '''
        Export the policy as a 2 dimensional list of actions.
        '''
        a = [[0]*12 for i in range(12)]
        for i in range(12):
            for t in range(12):
                a[i][t] = self.policy((i,t))
        return a

    def agent_init(self, task_spec):
        """Re-initialize the agent for a new training round."""
        #Reset the Q-values
        self.Q = {}

    def agent_start(self, state):
        """ Called every time a new game is started """
        state = tuple(state.intArray)
        return self.do_step(state)

    def agent_step(self, reward, state):
        """ Called for each game step """
        state = tuple(state.intArray)
        return self.do_step(state, reward)


    def agent_end(self, reward):
        """ Called when a game ends, this is where we learn """

    def agent_cleanup(self):
        """ Clean up for next run """

    def agent_message(self, msg):
        """ Retrieve message from the environment in the form param=value """
        result = re.match('(.+)=(.+)', msg)
        if result:
            param, value = result.groups()
            if param == 'echo' and value != 'None':
                return value
            elif param == 'export_policy':
                return self.export_policy()
            elif param == 'get_name':
                return self.name
            elif param == 'alpha' and value != 'None' and \
            type(value) in (int, float):
                self.alpha is value
            elif param == 'epsilon' and value != 'None' and \
            type(value) in (int, float):
                self.epsilon = value

            else:
                return "Unknown parameter: " + param

        else:
            return "Unknown command: " + msg;

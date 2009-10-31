'''
Created on Oct 31, 2009

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''

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
import math
import random
from copy import copy

from rlglue.agent.Agent import Agent
from rlglue.types import Action
from rlglue.types import Observation
from rlglue.agent import AgentLoader as AgentLoader


class GradientAgent(Agent):
    """
    Base agent for TD learning.
    """

    #The 4 actions we can take.
    actions = [('E',), ('N',), ('S',), ('W',)]

    #Discount factor Alpha
    alpha = 0.1
    
    name = 'gradient'
    
    #Number of rewards seen so far (for the baseline)
    num_rewards = 0
    baseline = 0.0
    
    #We need to remember our last action and state for updating the thetas
    last_state = []
    last_action = []

    def update_theta(self, state, action, reward):
        t_x = self.theta_x[state[0]][action]
        t_y = self.theta_y[state[1]][action]
        
        #The delta part is the same for both theta values:
        d_theta = self.alpha * (reward - self.baseline) * \
                    (1 - self.policy_val(state, action))
#        print "Reward: ", reward
#        print "Delta: ", d_theta
#        print "Base: ", self.baseline
#        print "C: ", 1 - self.policy_val(state, action)
        t_x = t_x + d_theta
        t_y = t_y + d_theta
        self.theta_x[state[0]][action] = t_x
        self.theta_y[state[1]][action] = t_y
                    

    def update_avg_reward(self, reward):
        self.baseline = (self.baseline * self.num_rewards + float(reward) ) / \
                            (self.num_rewards + 1)
        self.num_rewards += 1
     
    def policy_val(self, state, action, pol_denom = None):
        '''
        Calculate the actual soft-max likelihood of the state-action pair.
        The denominator of the soft-max formula can be pre-calculated and 
        passed if this function is to be called many times in the same place.
        '''
        if pol_denom is None:
            pol_denom = 0
            for action in self.actions:
                pol_denom += math.exp(self.theta_x[state[0]][action] + \
                                      self.theta_y[state[1]][action])

        theta = self.theta_x[state[0]][action] + self.theta_y[state[1]][action]
        print 'State: ', state
        print 'Action: ', action
        print 'Theta: ', theta
        return math.exp(theta) / pol_denom
    
    def pick_weighted(self, weighted_dict):
        '''
        Pick a random action from a weighted distribution.
        '''
        rand = random.random()
        last_el = 0
        idx = weighted_dict.keys()
        idx.sort()
        for i in idx:
            print i
            if last_el <= rand and rand <= i:
                return weighted_dict[i]
            last_el = i
            
        #If nothing has been picked it means it hit a bit too high, so return
        #the highest valued function.
        return weighted_dict[max(weighted_dict)]
        
    def policy(self, state):
        """
        Return the action to be taken for the state given using soft-max.
        """
        
        #The denominator of the policy, aka the sum of the exp for each pref.
        pol_denom = 0
        for action in self.actions:
            pol_denom += math.exp(self.theta_x[state[0]][action] + self.theta_y[state[1]][action])
        
        #Calculate the value of the policy for each state
        pol_vals = []
        for action in self.actions:
            theta = self.theta_x[state[0]][action] + self.theta_y[state[1]][action]
            pol_vals.append((action, math.exp(theta) / pol_denom))
        
        print pol_vals
        ranges = {}
        last_val = 0
        for val in pol_vals:
            ranges[val[1] + last_val] = val[0]
            last_val = val[1] + last_val
        print ranges
        return self.pick_weighted(ranges)


    def do_step(self, state, reward = None):
        """
        Runs the actual Q-Learning algorithm.
        In a separate function so it can be called both on start and on step.
        """
        a_obj = Action()
        #Query the policy to find the best action
        action = self.policy(state)
        a_obj.charArray = list(action)
        print 'action: ', action
        #Run the Q update if this isn't the first step
        if reward is not None:
            self.update_theta(tuple(self.last_state), tuple(self.last_action), reward)
            #Update the average reward
            self.update_avg_reward(reward)
        #Save the current state-action pair for the next step's Q update.
        self.last_state = state
        self.last_action = action
        #And we're done
        return a_obj

    def export_policy(self):
        '''
        Export the policy as a 2 dimensional list of actions.
        '''
        #Get the softmax evaluation for each action in this state
        #and pick the 'best' action based on the softmax value.
        #This allows us to export a determenistic policy.

        a = [[0]*12 for i in range(12)]
        for i in range(12):
            for t in range(12):
                acts = {}
                for action in self.actions:
                    print 'Value: ', self.policy_val((i, t), action)
                    acts[self.policy_val((i, t), action)] = action
                print acts
                a[i][t] = acts[max(acts.keys())]
                print a[i][t]
        return a

    def agent_init(self, task_spec):
        """Re-initialize the agent for a new training round."""
        #Reset the Theta values
        actions_dict = dict((a,random.random()) for a in self.actions)
        self.theta_x = dict((i,copy(actions_dict)) for i in range(12))
        self.theta_y = dict((i,copy(actions_dict)) for i in range(12))

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
        pass

    def agent_cleanup(self):
        """ Clean up for next run """
        actions_dict = dict((a,0) for a in self.actions)
        self.theta_x = dict((i,copy(actions_dict)) for i in range(12))
        self.theta_y = dict((i,copy(actions_dict)) for i in range(12))  

    def agent_message(self, msg):
        """ Retrieve message from the environment in one of the forms
        get_param or param=value """

        result = re.match('(.+)=(.+)', msg)
        if result:
            param, value = result.groups()
            if param == 'echo' and value != 'None':
                return value
            elif param == 'alpha' and value != 'None' and \
            type(value) in (int, float):
                self.alpha is value

            else:
                return "Unknown parameter: " + param
        elif msg == 'get_name':
            return self.name
        elif msg == 'get_q':
            return repr(list())
        elif msg == 'get_policy':
            policy = self.export_policy()
            return str(policy)
        else:
            return "Unknown command: " + msg;

if __name__=="__main__":
    AgentLoader.loadAgent(GradientAgent())

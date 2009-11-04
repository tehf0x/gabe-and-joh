"""
MC Policy Gradient Agent

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

from base import BaseAgent

class GradientAgent(BaseAgent):
    """
    MC Policy Gradient agent
    """

    # Name of this agent
    name = 'MC-Policy-Gradient'
    
    # The 4 actions we can take.
    # TODO: Should be moved to taskSpec!
    actions = [('E',), ('N',), ('S',), ('W',)]

    # Discount Gamma value
    # TODO: Should be moved to taskSpec
    gamma = 0.9
    
    # Learning rate alpha
    alpha = 0.01
    
    # Epsilon-Greed epsilon value
    epsilon = 0.1
    
    # Epsilon is multiplied by this parameter for each episode
    #epsilon_mul = 0.9993
    epsilon_mul = 1.0

    # We need to remember our last action and state for updating Q
    last_state = ()
    last_action = ()
    
    # Number of rewards seen so far (for the baseline)
    num_rewards = 0
    baseline = 0.0
    
    def agent_init(self, task_spec):
        """ Initialize the agent """
        pass
        
    def agent_start(self, state):
        """ Called every time a new episode is started """
        #self.baseline = 0.0
        #self.num_rewards = 0
        state = tuple(state.intArray)
        return self.do_step(state)

    def agent_step(self, reward, state):
        """ Called for each step in the episode """
        state = tuple(state.intArray)
        return self.do_step(state, reward)

    def agent_end(self, reward):
        """ Called when a game ends """
        #self.delta += self.rewards * self.z
        self.theta_x += self.alpha * delta / self.num_rewards
        self.theta_y += self.alpha * delta / self.num_rewards

    def agent_cleanup(self):
        """ Clean up for next experiment """
        actions_dict = dict((a,0) for a in self.actions)
        self.theta_x = dict((i,copy(actions_dict)) for i in range(12))
        self.theta_y = dict((i,copy(actions_dict)) for i in range(12))
        
        self.avg_reward = 0
        self.num_rewards = 0
    
    def update_theta(self, state, action, reward):
        """ Update our theta parameters with a new trajectory """
        row, col = state
        
        t_x = self.theta_x[col]
        t_y = self.theta_y[row]
        
        d_theta = {}
        # The delta is the same for both theta values:
        for a in actions:
            d = 0
            if a == action:
                d = 1
            d_theta[a] =  (d - self.policy_val(state, action))

        
        for a in actions:
            t_x[a] += d_theta[a]
            t_y[a] += d_theta[a]
        
        self.avg_reward = self.avg_reward + (1.0 / self.num_rewards) \
                         * (reward - self.avg_reward)
        self.theta_x[col][action] = t_x
        self.theta_y[row][action] = t_y
                    

    def update_avg_reward(self, reward):
        """ Update average reward baseline """
        self.baseline = (self.baseline * self.num_rewards + float(reward) ) / \
                            (self.num_rewards + 1)
        self.num_rewards += 1
     
    def policy_val(self, state, action):
        """
        Calculate the soft-max likelihood of a state-action pair.
        """
        row, col = state
        
        pol_denom = 0
        for a in self.actions:
            pol_denom += math.exp(self.theta_x[col][a] + self.theta_y[row][a])

        theta = self.theta_x[col][action] + self.theta_y[row][action]
        #print 'State: ', state
        #print 'Action: ', action
        #print 'Theta: ', theta
        return math.exp(theta) / pol_denom
    
    def pick_weighted(self, weighted_dict):
        """ Pick a random element from a weighted distribution.
        
        weighted_dist is a dictionary where the keys are the elements
        to pick and the values are the weights of picking the element.
        
        For example:
        weighted_dict[A] = 0.3
        weighted_dict[B] = 0.7
        
        Would pick A 30% and B 70% of the time.
        """
        
        weight_total = float(sum(weighted_dict.values()))
        
        dice = random.random()
        lower = 0
        
        for e, w in weighted_dict.items():
            p = float(w) / weight_total # Probability of selecting w
            #print 'e:',e,'w:',w,'p:',p,'lower:',lower
            #print 'check: dice(%f) >= lower(%f) and dice(%f) < (lower + p)(%f)' % (dice, lower, dice, lower + p)
            if dice >= lower and dice < lower + p:
                return e
            lower += p
        
        # Shouldn't be reached
        raise ValueError
        
    
    def pick_weighted2(self, weighted_dict):
        """
        Pick a random action from a weighted distribution.
        """
        rand = random.random()
        last_el = 0
        idx = weighted_dict.keys()
        idx.sort()
        for i in idx:
            #print i
            if last_el < rand and rand <= i:
                return weighted_dict[i]
            last_el = i
            
        #If nothing has been picked it means it hit a bit too high, so return
        #the highest valued function.
        return weighted_dict[max(weighted_dict)]
        
    def policy(self, state):
        """
        Return the action to be taken for the state given using soft-max.
        """
        
        # Calculate the value of the policy for each state
        pol_vals = {}
        for action in self.actions:
            pol_vals[action] = self.policy_val(state, action)
        
        #if state == (11,0):
        #    print 'POL_VALS for', state, ':', pol_vals
        
        #print pol_vals
        #ranges = {}
        #last_val = 0
        #for val in pol_vals:
        #    ranges[val[1] + last_val] = val[0]
        #    last_val = val[1] + last_val
        #print ranges
        return self.pick_weighted(pol_vals)


    def do_step(self, state, reward = None):
        """ Make an action from state, given an optional (previous) reward
        
        In a separate function so it can be called both on start and on step.
        """
        a_obj = Action()
        
        # Query the policy to find the best action
        action = self.policy(state)
        a_obj.charArray = list(action)
        
        #print 'action: ', action
        
        # Run the parameter update if this isn't the first step
        if reward is not None:
            self.update_theta(tuple(self.last_state), tuple(self.last_action), reward)
            self.update_avg_reward(reward)
        
        '''
        p = self.export_policy()
        for row in p:
            for col in row:
                print col[0][0],
            print        
        print
        '''
        # Save the current state-action pair for the next step update.
        self.last_state = state
        self.last_action = action
        
        # Actionify!
        return a_obj

    def export_policy(self):
        """
        Export the policy as a 2 dimensional list of actions.
        """
        # Get the softmax evaluation for each action in this state
        # and pick the 'best' action based on the softmax value.
        # This allows us to export a determenistic policy.
        
        a = [[0]*12 for i in range(12)]
        for row in range(12):
            for col in range(12):
                pol_vals = {}
                for action in self.actions:
                    pol_vals[action] = self.policy_val((row, col), action)
                    #print 'Value: ', self.policy_val((i, t), action)
                #print acts
                a[row][col] = max(pol_vals.items(), key=lambda e: e[1])
                #print a[i][t]
        return a
    
    def agent_message_get_param(self, param):
        """ Get a parameter via message """
        if param == 'policy':
            return repr(self.export_policy())
        
        return BaseAgent.agent_message_get_param(self, param)

if __name__=="__main__":
    AgentLoader.loadAgent(GradientAgent())

"""
SARSA Agent

Authors:
    Johannes H. Jensen <johannj@stud.ntnu.no>
    Gabe Dulac-Arnold <gabe@squirrelsoup.net>

Agent settings can be modified real-time by sending messages to the
agent through RL-Glue. The format is <setting>=<value>
"""

from random import random,choice
from td_agent import TDAgent
from rlglue.agent import AgentLoader as AgentLoader


class SarsaAgent(TDAgent):
    """
    Implements Sarsa Learning in an agent.
    """
    
    name = 'SARSA'

    def update_Q(self, state, action, reward, new_state = None):
        """
        Update the Q value of this state-action pair.
        
        new_state is None when terminal state has been reached.
        """
        Q_val = self.Q[state][action]
        
        #Look at the best action from the next state.
        Qp_val = 0
        if new_state is not None:
            new_action = self.policy(new_state)
            Qp_val = self.Q[new_state][new_action]
        
        #The famous formula:
        Q_val = Q_val + self.alpha * (reward + self.gamma * Qp_val - Q_val)
        self.Q[state][action] = Q_val

if __name__=="__main__":
    AgentLoader.loadAgent(SarsaAgent())

"""
Sarsa Agent

See the README for details

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

    def update_Q(self, state, action, reward, new_state):
        """
        Update the Q value of this state-action pair.
        """
        #If it hasn't been visited yet, initialize it.
        try:
            Q_val = self.Q[state][action]
        except KeyError:
            self.Q[state] = {('E',) : random(), ('N',) : random(), ('S',) : random(), ('W',) : random()}
            Q_val = choice(self.Q[state].values())
        #Look at the best action from the next state.
        try:
            new_action = self.policy(new_state)
            Qp_val = self.Q[new_state][new_action]
        #If no state-action pairs exist for this state yet,
        #initialize the state then set Qp = 0
        except (KeyError, ValueError):
            self.Q[new_state] = {('E',) : random(), ('N',) : random(), ('S',) : random(), ('W',) : random()}
            Qp_val = choice(self.Q[new_state].values())
        #The famous formula:
        Q_val = Q_val + self.alpha * (reward + self.gamma * Qp_val - Q_val)
        self.Q[state][action] = Q_val

if __name__=="__main__":
    AgentLoader.loadAgent(SarsaAgent())

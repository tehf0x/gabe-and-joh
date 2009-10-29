"""
Q-Learning Agent

See the README for details

Authors:
    Johannes H. Jensen <johannj@stud.ntnu.no>
    Gabe Dulac-Arnold <gabe@squirrelsoup.net>

Agent settings can be modified real-time by sending messages to the
agent through RL-Glue. The format is <setting>=<value>
"""

from td_agent import TDAgent
from rlglue.agent import AgentLoader as AgentLoader


class QAgent(TDAgent):    
    """
    Implements Q-Learning in an agent.
    """
    
    def update_Q(self, state, action, reward, new_state):
        """
        Update the Q value of this state-action pair.
        """
        #If it hasn't been visited yet, initialize it.
        try:
            Q_val = self.Q[state][action]
        except KeyError:
            print 'ke'
            self.Q[state] = {('E',) : 0, ('N',) : 0, ('S',) : 0, ('W',) : 0}
            Q_val = 0
    
        #Look at the best action from the next state.
        try:       
            Qp_val = max(self.Q[new_state].values())
        #If no state-action pairs exist for this state yet,
        #initialize the state then set Qp = 0
        except (KeyError, ValueError):
            print 'ke2'
            self.Q[new_state] = {('E',) : 0, ('N',) : 0, ('S',) : 0, ('W',) : 0}
            Qp_val = 0
        #The famous formula:
        Q_val = Q_val + self.alpha * (reward + self.gamma * Qp_val - Q_val)
        print state, 'action: ', action
        print 'Q: ', self.Q[state]
        print 'Q val: ', Q_val
        self.Q[state][action] = Q_val

if __name__=="__main__":
    AgentLoader.loadAgent(QAgent())

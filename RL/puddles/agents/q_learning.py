"""
Q-Learning Agent

See the README for details

Authors:
    Johannes H. Jensen <johannj@stud.ntnu.no>
    Gabe Dulac-Arnold <gabe@squirrelsoup.net>

Agent settings can be modified real-time by sending messages to the
agent through RL-Glue. The format is <setting>=<value>
"""

from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.types import Observation


class QAgent(Agent):    
    """
    Implements Q-Learning in an agent.
    """
    
    def do_step(self, state, reward = False):
        """
        Runs the actual Q-Learning algorithm.
        In a separate function so it can be called both on start and on step.
        """
        
        a_obj = Action()
        a_obj.intArray = action
        
        return a_obj
    
    def agent_init(self, taskSpec):
        pass
    
    def agent_start(self, state):
        """ Called every time a new game is started """
        print "GAME START!"
        return self.do_step(state.intArray)
    
    def agent_step(self, reward, state):
        """ Called for each game step """
        state = tuple(state.intArray)
        return self.do_step(state)

    
    def agent_end(self, reward):
        """ Called when a game ends, this is where we learn """

                
    def agent_cleanup(self):
        """ Clean up for next run """
        
        self.save()
        
    
    def agent_message(self, msg):
        """ Retrieve message from the environment in the form param=value """
        result = re.match('(.+)=(.+)', msg)
        if result:
            param, value = result.groups()
            if param == 'save_to' and value != 'None':
                self.save_to = str(value)
            elif param == 'load_from' and value != 'None':
                self.load_from = str(value)
            else:
                return "Unknown parameter: " + param
            
        else:
            return "Unknown command: " + msg;


if __name__=="__main__":
    AgentLoader.loadAgent(QAgent())

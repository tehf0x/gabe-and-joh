"""
Base Agent class

Authors:
    Johannes H. Jensen <johannj@stud.ntnu.no>
    Gabe Dulac-Arnold <gabe@squirrelsoup.net>

Agent settings can be modified real-time by sending messages to the
agent through RL-Glue. The format is <setting>=<value>
"""

import re

from rlglue.agent.Agent import Agent
from rlglue.types import Action
from rlglue.types import Observation


class BaseAgent(Agent):
    """ Base Agent class """
    
    """ Name of the agent """
    name = 'BaseAgent'
    
    """ Whether to print debugging info """
    debug = True
    
    def __init__(self):
        pass
    
    def agent_init(self, task_spec):
        """ Initialize the agent """
        pass

    def agent_start(self, state):
        """ Called every time a new episode is started """
        pass

    def agent_step(self, reward, state):
        """ Called for each step in the episode """
        pass

    def agent_end(self, reward):
        """ Called when a game ends """
        pass

    def agent_cleanup(self):
        """ Clean up for next experiment """
        pass
    
    
    def debug(self, *args):
        """ Print a debug msg """
        if self.debug:
            print "%s: %s" % (self.name, ' '.join(args))
    
    def agent_message_set_param(self, param, value):
        """ Set a parameter via message """
        # Only support setting existing parameters
        attr = getattr(self, param)
        setattr(self, param, eval(value))
    
    def agent_message_get_param(self, param):
        """ Get a parameter via message """
        return str(getattr(self, param))
    
    def agent_message_handler(self, msg):
        """ Handle a custom message """
        raise ValueError('Unknown message: %s' % (msg))
    
    def agent_message(self, msg):
        """ Retrieve and handle a message
        
        Set parameters by sending a message in the form:
        
            set param value
            
        Custom setters can be handled by overloading agent_message_set_param.
        
        Get parameters by sendin a message in the form:
        
            get param
        
        Custom getters can be handled by overloading agent_message_get_param.
        
        Other messages can be handled by overloading agent_message_handler.
        """
        result = re.match('set (.+) (.+)', msg)
        if msg.startswith('set'):
            param, value = msg.split(None, 2)[1:]
            self.debug('set', param, value)
            
            self.agent_message_set_param(param, value)
        
        elif msg.startswith('get'):
            param = msg.split(None, 1)[1]
            
            return self.agent_message_get_param(param)
        
        else:
            return self.agent_message_handler(msg)
        
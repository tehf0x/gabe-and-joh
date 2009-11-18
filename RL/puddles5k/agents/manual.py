"""
Manual user-controlled agent for environment testing

@author: joh
"""

import curses

from rlglue import RLGlue
from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.types import Observation


class ManualAgent(Agent):    
    """
    Manual agent
    """
    # (string) -> void
    def agent_init(self, taskSpecification):
        self.window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.window.keypad(1)
    
    # (Observation) -> Action
    def agent_start(self, observation):
        return self.agent_step(0, observation)
    
    # (double, Observation) -> Action
    def agent_step(self, reward, observation):
        action = None
        
        self.window.erase()
        self.window.addstr('STATE: %s\n' % (observation.intArray))
        self.window.addstr('REWARD: %s\n' % (reward))
        self.window.addstr('HIT UP, DOWN, LEFT or RIGHT to move...\n')
        self.window.refresh()

        try:
            c = self.window.getch()
            if c == curses.KEY_UP:
                action = 'N'
            elif c == curses.KEY_DOWN:
                action = 'S'
            elif c == curses.KEY_LEFT:
                action = 'W'
            elif c == curses.KEY_RIGHT:
                action = 'E'
            
            self.window.refresh()
        
        except KeyboardInterrupt:
            RLGlue.RL_cleanup()
            
        
        a = Action()
        
        if action:
            a.charArray = [action]
        
        return a
    
    # (double) -> void
    def agent_end(self, reward):
        pass
    
    # () -> void
    def agent_cleanup(self):
        curses.endwin()
        print 'BYE!'

    # (string) -> string
    def agent_message(self, message):
        pass

if __name__=="__main__":
    AgentLoader.loadAgent(ManualAgent())

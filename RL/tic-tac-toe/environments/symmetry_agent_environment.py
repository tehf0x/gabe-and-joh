"""
MENACE agent environment wrapper
"""

import sys

# Ugly!
sys.path.append('../')

from agents.symmetry_agent import SymmetryAgent
from wrapper_environment import WrapperEnvironment
from rlglue.environment import EnvironmentLoader

class SymmetryEnvironment(WrapperEnvironment, SymmetryAgent):
    
    name = 'symmetry_agent'
    
    player = 2
    def env_play(self): 
        action = self.do_step(self.state)
        self.state = action.intArray
        

if __name__ == "__main__":
    EnvironmentLoader.loadEnvironment(SymmetryEnvironment())
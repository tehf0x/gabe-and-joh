from exceptions import Exception

from rlglue.environment.Environment import Environment
from rlglue.environment import EnvironmentLoader as EnvironmentLoader
from rlglue.types import Observation
from rlglue.types import Action
from rlglue.types import Reward_observation_terminal

class WrapperEnvironment(Environment):

    name = 'wrapper'

    def env_init(self):
        self.color = 2
        return "VERSION RL-Glue-3.0 PROBLEMTYPE episodic " + \
        "DISCOUNTFACTOR 1.0 OBSERVATIONS INTS (9 0 2)" +\
        "ACTIONS INTS (9 0 2) REWARDS (0 1) EXTRA"

    def env_play(self):
        pass

    def is_victory(self):
        """
        Check for victory by looking at all the ways someone could win.
        """
        lines = ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), \
                (0,4,8), (2,4,6))
        for line in lines:
            if self.state[line[0]] == self.state[line[1]] == self.state[line[2]] != 0:
                return True

        return False

    def is_full(self):
        """
        Check if the board is full.
        """
        print "Checking full:", self.state
        for i in self.state:
            if(i == 0):
                return False
        return True

    def env_start(self):
        """
        Get the state of the environment and return it.
        """
        self.state = [0 for i in range(9)]

        obs = Observation()
        obs.intArray = self.state

        return obs

    def env_step(self,actions):
        """
        Verify the actions are valid, play a move, and return the state.
        """
        reward = 0
        terminal = 0

        #Change our current state to the new board
        self.state = actions.intArray
        #Check if the agent made a winning move
        if self.is_victory():
            print "WE LOST"
            reward = 1
            terminal = 1
        #Otherwise keep on playing!
        elif self.is_full():
            "AGENT FILLED"
            reward = 1
            terminal = 1

        elif not self.is_full():
            print "PLAY"
            self.env_play()

            #Check if we won
            if self.is_full():
                print "WE FILLED"
                reward = 1
                terminal = 1
                
            if self.is_victory():
                print "WE WON"
                reward = 0
                terminal = 1
            
                

        #Set up the observation object and return it
        obs = Observation()
        obs.intArray = self.state

        reward_obs = Reward_observation_terminal()
        reward_obs.r = reward
        reward_obs.o = obs
        reward_obs.terminal = terminal
        return reward_obs

    def env_cleanup(self):
        pass
    
    def env_message(self, mesg):
        cases = {'ping' : lambda : 'pong',
                 'name' : lambda : self.name}
        
        return cases[mesg]()

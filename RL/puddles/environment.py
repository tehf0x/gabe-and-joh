"""
Puddle world environment

@author: joh
"""

import random
import re

from rlglue.environment.Environment import Environment
from rlglue.environment import EnvironmentLoader
from rlglue.types import Observation, Action, Reward_observation_terminal

class PuddleState():
    
    def __init__(self, reward=0, start=False, terminal=False, wind=(0.5, [0, 1])):
        """ Create a new puddle state
        
        When reaching the state, a reward will be granted. The state might
        also be a start state or a terminal state. Finally, a wind might be 
        present in the state represented by a tuple (prob, speed). 
        That is, the agent will be pushed in the direction of speed with a 
        probability prob.
        """
        self.reward = reward
        self.start = start
        self.terminal = terminal
        self.wind = wind
    
    def __str__(self):
        return str(self.reward)

class PuddleWorld(list):
    
    def __init__(self, size=(12,12)):
        self.agent_state = None
        
        # Initialize with empty PuddleStates
        for row in range(size[0]):
            self.append([])
            for col in range(size[1]):
                self[row].append(PuddleState())
    
    def add_starts(self, *args):
        for row, col in args:
            self[row][col].start = True
    
    def add_terminals(self, *args):
        for row, col in args:
            self[row][col].terminal = True
    
    def add_rewards(self, *args):
        for (row, col), reward in args:
            self[row][col].reward = reward
    
    def __str__(self):
        s = ''
        for row, states in enumerate(self):
            for col, state in enumerate(states):
                if self.agent_state == [row, col]:
                    t = 'A'
                elif state.start:
                    t = 'S'
                elif state.terminal and state.reward is 0:
                    t = 'T'
                else:
                    #if state.reward is 0:
                    #    t = '_'
                    #else:
                    t = str(state.reward)
                
                s += t.rjust(2).center(3)
                
            s += "\n"
        
        return s

class PuddleEnvironment(Environment):
    
    """ Gridworld size (y, x) """
    size = (12, 12)
    
    """ Valid actions and their resulting movement vectors (y, x) """
    valid_actions = {'N': (-1, 0),
                     'S': (1, 0),
                     'W': (0, -1),
                     'E': (0, 1)}
    
    """ Action success probability """
    action_prob = 0.9
    
    """ Start states """
    start_states = [(5,0), (6,0), (10,0), (11,0)]
    
    """ Terminal states """
    terminal_states = {(0,11): 10}
    
    """ Rewards """
    rewards = [[0, 0, 0,  0,  0,  0,  0,  0,  0, 0, 0, 0], \
               [0, 0, 0,  0,  0,  0,  0,  0,  0, 0, 0, 0], \
               [0, 0, 0, -1, -1, -1, -1, -1, -1, 0, 0, 0], \
               [0, 0, 0, -1, -2, -2, -2, -2, -1, 0, 0, 0], \
               [0, 0, 0, -1, -2, -3, -3, -2, -1, 0, 0, 0], \
               [0, 0, 0, -1, -2, -3, -2, -2, -1, 0, 0, 0], \
               [0, 0, 0, -1, -2, -3, -2, -1,  0, 0, 0, 0], \
               [0, 0, 0, -1, -2, -2, -2, -1,  0, 0, 0, 0], \
               [0, 0, 0, -1, -1, -1, -1, -1,  0, 0, 0, 0], \
               [0, 0, 0,  0,  0,  0,  0,  0,  0, 0, 0, 0], \
               [0, 0, 0,  0,  0,  0,  0,  0,  0, 0, 0, 0], \
               [0, 0, 0,  0,  0,  0,  0,  0,  0, 0, 0, 0]]
    
    # () -> string
    def env_init(self):
        # Create gridworld
        self.world = PuddleWorld(self.size)
        
        # Set up rewards
        for row in range(len(self.rewards)):
            for col in range(len(self.rewards[row])):
                self.world[row][col].reward = self.rewards[row][col]
        
        return 'PuddleEnvironment initialized...'
    
    # () -> Observation
    def env_start(self):
        """ Start the game! """
        # Set up start states
        self.world.add_starts(*self.start_states)
        
        # Set up terminal states
        self.world.add_terminals(*self.terminal_states.keys())
        for (row, col), reward in self.terminal_states.items():
            self.world[row][col].reward = reward
        
        # Initialize state of the agent to one of start_states
        r = random.randrange(len(self.start_states))
        self.world.agent_state = list(self.start_states[r])
        
        print('START WORLD:')
        print(self.world)
        
        # Pass agent state over to the agent
        obs = Observation()
        obs.intArray = self.world.agent_state

        return obs
    
    
    def enforce_world_bounds(self, state):
        """ Enforce world bounds """
        if state[0] < 0:
            state[0] = 0
        
        if state[0] >= len(self.world):
            state[0] = len(self.world) - 1
        
        if state[1] < 0:
            state[1] = 0
        
        if state[1] >= len(self.world[0]):
            state[1] = len(self.world[0]) - 1
    
    def move_agent(self, direction):
        """ Move agent in direction """
        self.world.agent_state[0] += direction[0]
        self.world.agent_state[1] += direction[1]
        
        # Enforce world bounds
        self.enforce_world_bounds(self.world.agent_state)
    
    # (Action) -> Reward_observation_terminal
    def env_step(self, action):
        # Action is one of N,S,W,E
        action = action.charArray[0]
        
        print 'ACTION:', action
        
        if not action in self.valid_actions.keys():
            print 'WARNING: Invalid action %s' % (action)
            obs = Observation()
            obs.intArray = self.world.agent_state
            return Reward_observation_terminal(0, obs, False)
        
        # The actions might result in movement in a direction other than the one 
        # intended with a probability of (1 - action_prob)
        dice = random.random()
        if dice > self.action_prob:
            # Randomness! Choose uniformly between each other action
            other_actions = list(set(self.valid_actions.keys()) - set(action))
            action = random.choice(other_actions)
        
        # Move the agent
        print 'RESULT ACTION:', action
        
        self.move_agent(self.valid_actions[action])
        
        # Apply wind from the new state
        pstate = self.world[self.world.agent_state[0]][self.world.agent_state[1]]
        if pstate.wind:
            p, dir = pstate.wind
            dice = random.random()
            if dice <= p:
                # Fudge & crackers! Our agent gets caught by the wind!
                print 'WIND IN %s!' % (dir)
                self.move_agent(dir)
        
        pstate = self.world[self.world.agent_state[0]][self.world.agent_state[1]]
        
        print 'NEW STATE:', str(self.world.agent_state)
        
        # Return observation
        obs = Observation()
        obs.intArray = self.world.agent_state
        
        print('IT\'S A NEW WORLD:')
        print(self.world)
        
        return Reward_observation_terminal(pstate.reward, obs, pstate.terminal)
        
        
    
    # () -> void
    def env_cleanup(self):
        pass
    
    # (string) -> string
    def env_message(self, msg):
        print 'ENV MSG', msg
        if msg == 'peek':
            # Peek at world state
            return str(self.world)
        
        # Look for prop=value
        result = re.match('(.+)=(.+)', msg)
        if result:
            param, value = result.groups()
            if param == 'terminal_states':
                self.terminal_states = eval(value)
            else:
                return "Unknown parameter: " + param
            
        else:
            return "Unknown command: " + msg;

if __name__ == '__main__':
    #p = PuddleEnvironment()
    #p.env_start()
    EnvironmentLoader.loadEnvironment(PuddleEnvironment())

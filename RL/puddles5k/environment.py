#!/usr/bin/env python
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
    
    def __repr__(self):
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
    
    """ Enable wind """
    enable_wind = True
    
    """ Enable stochastic actions """
    enable_stochastic_actions = True
    
    """ Step limit - sends terminal signal if reached """
    step_limit = 500
    
    """ Name of the environment """
    name = 'PuddleEnvironment'
    
    """ Whether to print debugging info """
    degug = True
    
    """ Output info about every step """
    output_steps = False
    
    # () -> string
    def env_init(self):
        # Create gridworld
        self.world = PuddleWorld(self.size)

        # Set up rewards
        for row in range(len(self.rewards)):
            for col in range(len(self.rewards[row])):
                self.world[row][col].reward = self.rewards[row][col]

        #return 'PuddleEnvironment initialized...'
        return ''

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
        
        # Initialize step counter
        self.steps = 0
        
        self.step_out('START WORLD:')
        self.step_out(self.world)
        
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
        self.steps += 1
        
        # Action is one of N,S,W,E
        action = action.charArray[0]

        self.step_out('ACTION:', action)

        if not action in self.valid_actions.keys():
            print 'WARNING: Invalid action %s' % (action)
            obs = Observation()
            obs.intArray = self.world.agent_state
            return Reward_observation_terminal(0, obs, False)

        # The actions might result in movement in a direction other than the one
        # intended with a probability of (1 - action_prob)
        if self.enable_stochastic_actions:
            dice = random.random()
            if dice > self.action_prob:
                # Randomness! Choose uniformly between each other action
                other_actions = list(set(self.valid_actions.keys()) - set(action))
                action = random.choice(other_actions)
            
            # Move the agent
            self.step_out('RESULT ACTION:', action)

        self.move_agent(self.valid_actions[action])

        # Apply wind from the new state
        if self.enable_wind:
            pstate = self.world[self.world.agent_state[0]][self.world.agent_state[1]]
            if pstate.wind:
                p, dir = pstate.wind
                dice = random.random()
                if dice <= p:
                    # Fudge & crackers! Our agent gets caught by the wind!
                    self.step_out('WIND IN %s!' % (dir))
                    self.move_agent(dir)
        
        
        pstate = self.world[self.world.agent_state[0]][self.world.agent_state[1]]

        # Return observation
        obs = Observation()
        obs.intArray = self.world.agent_state

        #print('IT\'S A NEW WORLD:')
        self.step_out(self.world)
        #self.debug('\n' + str(self.world))
        self.step_out("REWARD:", pstate.reward)
        
        terminal = pstate.terminal
        if self.steps > self.step_limit:
            self.debug("STEP LIMIT REACHED!")
            terminal = True

        return Reward_observation_terminal(pstate.reward, obs, terminal)



    # () -> void
    def env_cleanup(self):
        pass
    
    def env_message_set_param(self, param, value):
        """ Set a parameter via message """
        # Only support setting existing parameters
        attr = getattr(self, param)
        setattr(self, param, eval(value))
    
    def env_message_get_param(self, param):
        """ Get a parameter via message """
        return repr(getattr(self, param))
    
    def env_message_handler(self, msg):
        """ Handle a custom message """
        if msg == 'peek':
            return str(self.world)
        else:
            raise ValueError('Unknown message: %s' % (msg))
    
    def env_message(self, msg):
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
            
            self.env_message_set_param(param, value)
        
        elif msg.startswith('get'):
            param = msg.split(None, 1)[1]
            
            return self.env_message_get_param(param)
        
        else:
            return self.env_message_handler(msg)
    
    def debug(self, *args):
        """ Print a debug msg """
        if self.debug:
            args = [str(a) for a in args]
            print "%s: %s" % (self.name, ' '.join(args))
    
    def step_out(self, *args):
        if self.output_steps:
            args = [str(a) for a in args]
            print ' '.join(args)
    
if __name__ == '__main__':
    #p = PuddleEnvironment()
    #p.env_start()
    EnvironmentLoader.loadEnvironment(PuddleEnvironment())

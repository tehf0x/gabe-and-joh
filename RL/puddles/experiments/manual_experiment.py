"""
Manual experiment for testing the environment
"""

import sys
import os
import time

from rlglue import RLGlue

# Initialize RL Glue
RLGlue.RL_init()

RLGlue.RL_start()

running = True
reward = 0
while running:
    result = RLGlue.RL_step()
    running = not result.terminal

steps = RLGlue.RL_num_steps()
R = RLGlue.RL_return()

print 'Experiment ended after %d steps with a return of %d' % (steps, R)

RLGlue.RL_cleanup()
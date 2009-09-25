#!/usr/bin/python
'''
Created on Sep 24, 2009

File that actually runs the experiments.

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''


from value_methods import value_iteration
from graph_gen import graph_vals

v1 = value_iteration(sweeps=1)
v10 = value_iteration(sweeps=10)
v_f = value_iteration(theta=0.01)

graph_vals(v1, 'One Iteration')
graph_vals(v10, 'Ten Iterations')
graph_vals(v_f, 'Convergence')
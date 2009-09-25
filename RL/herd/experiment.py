#!/usr/bin/python
'''
Created on Sep 24, 2009

File that actually runs the experiments.

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''


from value_methods import value_iteration, policy_iteration
from graph_gen import graph_vals
'''
#
# Value Iteration
#

v1 = value_iteration(gamma=0.9, sweeps=1)
v10 = value_iteration(gamma=0.9, sweeps=10)
v_f = value_iteration(gamma=0.9, theta=0.01)

graph_vals(v1, 'Sweep 1')
graph_vals(v10, 'Sweep 10')
graph_vals(v_f, 'Optimal V*')

#
# Policy Iteration
#
values = []
V, pi = policy_iteration(gamma=0.9, theta=0.01, value_list=values)

for i, v in enumerate(values):
    graph_vals(v, 'Policy Evaluation %d' % (i + 1))
'''
    
#Gamma Variations
print 'Generating Gamma Variations'
for g in(0.9, 0.5, 0.3):
    values = []
    V, pi = policy_iteration(theta=0.01, value_list=values, gamma=g)
    
    print 'gamma = %f:' % (g)
    
    for s in ((4,7,1), (1,3,6), (9,2,1)):
        print 'state %s => action %s' % (s, pi[s])
    
'''    
    for i, v in enumerate(values):
        graph_vals(v, 'Policy Evaluation %d. Gamma: %f' % (i + 1, g))
'''
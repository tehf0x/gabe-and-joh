#
# Tic-Tac-Toe experiment settings
#

# 
# Experiment settings
#

experiment = dict(
    # Number of instances to run
    instances = 1,
    
    # Number of episodes (i.e. games) to run for each instance
    episodes = 10000,
    
    # Where to store results
    results_dir = 'results'
)


#
# Agent settings
#
agent = dict(
    # Alpha
    alpha = 0.01
)

#
# Environment settings
#
environment = dict(
    # Terminal states in the form (row,col): reward
    terminal_states = {(0,11): 10}  # A
    #terminal_states = {(2,9): 10}   # B
    #terminal_states = {(6,7): 10}   # C
    
)

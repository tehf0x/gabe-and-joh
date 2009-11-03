#
# Tic-Tac-Toe experiment settings
#

# 
# Experiment settings
#

experiment = dict(
    # Number of instances to run
    instances = 2,
    
    # Number of episodes (i.e. games) to run for each instance
    episodes = 2,
    
    # Where to store results
    results_dir = 'results'
)


#
# Agent settings
#
agent = dict(
    # Alpha
    alpha = 0.1,
    
    # Epsilon
    epsilon = 0.1
    
)

#
# Environment settings
#
environment = dict(
    # Enable wind
    enable_wind = False,
    
    # Enable stochastic actions
    enable_stochastic_actions = False,
    
    # Terminal states in the form (row,col): reward
    terminal_states = {(0,11): 10},  # A
    #terminal_states = {(2,9): 10}   # B
    #terminal_states = {(6,7): 10}   # C
    
    # Output info about every step
    #output_steps = True
)

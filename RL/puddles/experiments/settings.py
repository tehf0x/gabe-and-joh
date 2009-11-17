#
# Tic-Tac-Toe experiment settings
#

# 
# Experiment settings
#

experiment = dict(
    # Number of instances to run
    instances = 30,
    
    # Number of episodes (i.e. games) to run for each instance
    episodes = 5000,
    
    # Where to store results
    results_dir = 'results',
    
    # Epsilon-Greed epsilon value
    # Divide experiment into 3: high, decr, low
    # During high: keep epsilon constant at epsilon_high
    # During decr: decrease epsilon linearly until epsilon_decr
    # During low: keep epsilon constant at epsilon_low
    #epsilon_high = 0.8,
    #epsilon_decr = 0.2,
    #epsilon_low = 0.1,
)


#
# Agent settings
#
agent = dict(
    # Alpha
    alpha = 0.005,
    
    # Epsilon
    #epsilon = experiment['epsilon_high']
    epsilon = 0.1
    
)

#
# Environment settings
#
environment = dict(
    # Enable wind
    enable_wind = True,
    
    # Enable stochastic actions
    enable_stochastic_actions = False,
    
    # Terminal states in the form (row,col): reward
    terminal_states = {(0,11): 10},  # A
    #terminal_states = {(2,9): 10},   # B
    #terminal_states = {(6,7): 10},   # C
    
    # Output info about every step
    output_steps = False
)

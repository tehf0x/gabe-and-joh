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
    episodes = 100,
    
    # Where to store results
    results_dir = 'results'
)


#
# Agent settings
#
agent = dict(
    # Alpha
    alpha = 0.001
)

#
# Environment settings
#
environment = dict(
    # Terminal states in the form (row,col): reward
    terminal_states = {(0,11): 10}
    
)
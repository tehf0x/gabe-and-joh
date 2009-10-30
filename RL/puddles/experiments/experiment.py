#!/usr/bin/env python
"""
Puddles experiment

Authors:
    Johannes H. Jensen <johannj@stud.ntnu.no>
    Gabe Dulac-Arnold <gabe@squirrelsoup.net>


Runs a number of instances. Each instance consists of running a number
of episodes. Each episode is run until a terminal state is reached.
The results for each nth episode are averaged over the other instances.
This is to get a good average as each instance will differ.
"""

import sys
import os
import time
import pickle

import rlglue.RLGlue as RLGlue

class ProgressOutput:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.prev_length = 0
    
    def out(self, string):
        # Erase previous line
        bs = ''
        if self.prev_length > 0:
            bs = '\b' * (self.prev_length + 1)
        
        print bs + string,
        sys.stdout.flush()
        self.prev_length = len(string)
    
    

class Experiment:
    """ Experiment class
    Will run a number of episodes (100 by default) and collect results:
    
    - The number of steps in each episode
    - The reward for each episode
    
    The results can be collected as a string with get_result_data() """
    
    # Number of episodes to run
    episodes = 100
    
    # Episode counter
    episode_number = 0
    
    # Total reward
    total_reward = 0
    
    # Instance number
    instance = 0
    
    # Whether we have initialized RLGlue before
    has_inited = False
    
    # Whether to print progress output
    quiet = False
    
    def __init__(self, episodes = 100):
        """ Initialize experiment """
        self.episodes = episodes
        self.returns = [0] * episodes
        self.steps = [0] * episodes
        
        self.po = ProgressOutput()
        
        RLGlue.RL_init()
        self.has_inited = True
    
    def print_progress(self, length, str):
        if self.quiet:
            return
        
        bs = '\b' * (length + 1)
        print bs + str,
        sys.stdout.flush()
    
    def run(self):
        """ Run the experiment """
        if self.has_inited:
            RLGlue.RL_cleanup()
        
        self.instance += 1
        self.total_reward = 0
        self.episode_number = 0
        
        self.po.reset()
        
        # Progress output:
        #if not self.quiet:
        #    print "Running experiment #%d with %d episodes..." % (self.instance, self.episodes),
        
        pad = len('%d' % self.episodes)
        fmt = '%' + str(pad) + 'd/%d'
        
        for i in xrange(self.episodes):
            self.run_episode()
            self.po.out(str(self))
        
        print
        
    def run_episode(self):
        """ Run a single episode """
        terminal = RLGlue.RL_episode(0)   # 0 - run until terminal
        steps = RLGlue.RL_num_steps()
        reward = RLGlue.RL_return()
        
        #print "\nEpisode %d\t %d steps\t reward: %d" % (self.episode_number, steps, reward)
        #print "Episode "+str(episode_number)+"\t "+str(totalSteps)+ " steps \t" + str(totalReward) + " total reward\t " + str(terminal) + " natural end"
    
        self.returns[self.episode_number] = (reward + self.returns[self.episode_number] * (self.instance - 1)) / self.instance
        self.steps[self.episode_number] = (steps + self.steps[self.episode_number] * (self.instance - 1)) / self.instance        
        
        self.episode_number += 1
    
    def __str__(self):
        """ Generate summary """
        return "Experiment #%d: %d/%d episodes completed" % (self.instance, self.episode_number, self.episodes)



# Run experiment
if __name__ == "__main__":
    
    import settings
    
    # Create a new experiment
    experiment = Experiment(settings.experiment['episodes'])
    
    # Set up environment
    print
    print "Environment settings:"
    for k,v in settings.environment.items():
        msg = '%s=%s' % (k, v)
        print "  ", msg 
        RLGlue.RL_env_message(msg)
    
    # Set up agent
    print "Agent settings:"
    for k,v in settings.agent.items():
        msg = '%s=%s' % (k, v)
        print "  ", msg 
        RLGlue.RL_agent_message(msg)
    
    print
    
    # Run experiments
    for i in xrange(settings.experiment['instances']):
        experiment.run()
        
        #print str(experiment)
        #print str(experiment.returns)
        #print str(experiment.steps)
    
    print
    
    # Store data to file
    returns = experiment.returns
    steps = experiment.steps
    policy = eval(RLGlue.RL_agent_message('get_policy'))
    
    def gen_filename(base, ext):
        yield base + ext
        counter = 1
        while True:
            yield base + '.' + str(counter) + ext
            counter += 1
    
    #env_name = RLGlue.RL_env_message('get_name')
    agent_name = RLGlue.RL_agent_message('get_name')
    
    basename = agent_name
    results_dir = settings.experiment['results_dir']
    ext = '.pickle'
    filename = None
    filepath = None
    file = None
    
    for f in gen_filename(basename, ext):
        filepath = os.path.join(results_dir, f)
        if not os.path.exists(filepath):
            filename = f
            file = open(filepath, 'w')
            break
    
    print "Storing returns, steps and policy into %s..." % (filepath),
    
    obj = dict(
        settings = {'experiment': settings.experiment,
                    'environment': settings.environment,
                    'agent': settings.agent},
        returns = returns,
        steps = steps,
        policy = policy
    )
    pickle.dump(obj, file)
    
    print "Done!"
    
    RLGlue.RL_cleanup()



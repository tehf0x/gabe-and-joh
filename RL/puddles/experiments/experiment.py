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

import rlglue.RLGlue as RLGlue


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
    
    def __init__(self, episodes = 100):
        """ Initialize experiment """
        self.episodes = episodes
        self.returns = [0] * episodes
        self.steps = [0] * episodes
        
        RLGlue.RL_init()
        self.has_inited = True
    
    def run(self):
        """ Run the experiment """
        if self.has_inited:
            RLGlue.RL_cleanup()
        
        self.instance += 1
        self.total_reward = 0
        self.episode_number = 0
        
        for i in xrange(self.episodes):
            self.run_episode()
        
    def run_episode(self):
        """ Run a single episode """
        terminal = RLGlue.RL_episode(0)   # 0 - run until terminal
        steps = RLGlue.RL_num_steps()
        reward = RLGlue.RL_return()
        
        #print "Episode %d\t %d steps\t reward: %d" % (self.episode_number, steps, reward)
        #print "Episode "+str(episode_number)+"\t "+str(totalSteps)+ " steps \t" + str(totalReward) + " total reward\t " + str(terminal) + " natural end"
    
        self.returns[self.episode_number] = (reward + self.returns[self.episode_number] * (self.instance - 1)) / self.instance
        self.steps[self.episode_number] = (steps + self.steps[self.episode_number] * (self.instance - 1)) / self.instance        
        
        self.episode_number += 1
    
    def __str__(self):
        """ Generate summary """
        return "Experiment #%d: %d/%d episodes completed." % (self.instance, self.episode_number, self.episodes)
    
    def get_result_data(self):
        """ Get result data as string """
        data = ''
        for x, y in enumerate(self.results):
            data += '%d %f\n' % (x, y)
        
        return data
    
    def save_result(self, filename):
        """ Save result data to file """
        f = open(filename, 'w')
        data = self.get_result_data()
        f.write(data)
        f.close()



# Run experiment
if __name__ == "__main__":
    
    import settings
    
    # Create a new experiment
    experiment = Experiment(settings.experiment['episodes'])
    
    # Set up environment
    print "Environment settings:"
    for k,v in settings.environment.items():
        msg = '%s=%s' % (k, v)
        print "\t", msg 
        RLGlue.RL_env_message(msg)
    
    # Set up agent
    print "Agent settings:"
    for k,v in settings.agent.items():
        msg = '%s=%s' % (k, v)
        print "\t", msg 
        RLGlue.RL_agent_message(msg)
    
    # Run experiments
    for i in xrange(settings.experiment['instances']):
        print "Running experiment #%d with %d episodes..." % (i + 1, settings.experiment['episodes']),
        sys.stdout.flush()
        experiment.run()
        
        # Experiment completed, show summary
        print "Done!"
        print str(experiment)
        print str(experiment.returns)
        print str(experiment.steps)
        
    
    # Store data to file
    '''
    env_name = RLGlue.RL_env_message('name')
    data_file = env_name + '_' + time.strftime('%Y-%m-%d_%H:%M:%S.dat')
    data_path = os.path.join(settings.results_dir, data_file)
    
    print
    print "Storing results into %s..." % (data_path),
    
    """ Save result data to file """
    f = open(data_path, 'w')
    
    f.write("# Settings:\n")
    for k in dir(settings):
        if k.startswith('__'):
            continue
        f.write("#   %s = %s\n" % (k, getattr(settings, k)))
    
    data = experiment.get_result_data()
    f.write(data)
    f.close()
    
    '''
    #experiment.save_result(data_path)
    print "Done!"
    
    RLGlue.RL_cleanup()



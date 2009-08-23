# 
# 
#

import sys
import os
import time

import rlglue.RLGlue as RLGlue


class Experiment:
	''' Class representing an experiment '''
	
	# Number of episodes to run
	episodes = 100
	
	# Episode counter
	episode_number = 0
	
	# Total accumulated reward
	total_reward = 0
	
	# Cumulative average of results
	results = []
	
	# Instance number
	instance = 0
	
	# Whether we have initialized RLGlue before
	has_inited = False
	
	def __init__(self, episodes = 100):
		self.episodes = episodes
		self.results = [0] * episodes
		
		RLGlue.RL_init()
		self.has_inited = True
	
	def run(self):
		''' Run the experiment '''
		if self.has_inited:
			RLGlue.RL_cleanup()
		
		self.instance += 1
		self.total_reward = 0
		self.episode_number = 0
		
		for i in xrange(self.episodes):
			self.run_episode()
		
	def run_episode(self):
		''' Run a single episode '''
		terminal = RLGlue.RL_episode(10)
		steps = RLGlue.RL_num_steps()
		reward = RLGlue.RL_return()
		
		#print "Episode %d\t %d steps\t reward: %d" % (episode_number, steps, reward)
		#print "Episode "+str(episode_number)+"\t "+str(totalSteps)+ " steps \t" + str(totalReward) + " total reward\t " + str(terminal) + " natural end"
	
		self.total_reward += reward
		
		# Update average
		x = self.total_reward / (self.episode_number + 1)
		self.results[self.episode_number] += (x - self.results[self.episode_number]) / self.instance
		#self.results.append(self.total_reward / self.episode_number)
		
		self.episode_number += 1
	
	def __str__(self):
		''' Generate summary '''
		return "Experiment #%d: %d/%d episodes completed. Accumulated reward: %d (%d%%)" % (self.instance, self.episode_number, self.episodes, self.total_reward, 100 * self.total_reward / self.episodes)
	
	def get_result_data(self):
		''' Get result data '''
		data = ''
		for x, y in enumerate(self.results):
			data += '%d %f\n' % (x, y)
		
		return data
		

# Run experiment
if __name__=="__main__":
	instances = 3
	episodes = 1000
	
	# Create a new experiment
	experiment = Experiment(episodes)
	data_dir = 'results'
	
	for i in xrange(instances):
		print "Running experiment #%d with %d episodes..." % (i + 1, episodes),
		sys.stdout.flush()
		experiment.run()
		
		# Experiment completed, show summary
		print "Done!"
		print str(experiment)
		
	
	# Store data to file
	env_name = RLGlue.RL_env_message('name')
	data_file = env_name + '_' + time.strftime('%Y-%m-%d_%H:%M:%S.dat')
	data_path = os.path.join(data_dir, data_file)
	
	print
	print "Storing results into %s..." % (data_path),
	f = open(data_path, 'w')
	data = experiment.get_result_data()
	f.write(data)
	f.close()
	
	print "Done!"
	
	RLGlue.RL_cleanup()


"""
MENACE experiment

Authors:
    Johannes H. Jensen <johannj@stud.ntnu.no>
    Gabe Dulac-Arnold <gabe@squirrelsoup.net>


Runs a number of instances. Each instance consists of running a set
of games. This is to get a good average as each instance will differ.

The game results (i.e. rewards) are collected and stored
as a cumulative average of games not lost against the number of games 
played.

The results are finally stored to file in a gnuplot friendly format:
each line is a space-separated list of numbers, where the first
number is the number of games played and the second is the
cumulative reward average.

See settings.py for modifying the behavior of the experiment and agent.
See results/plot.gnuplot for creating graphs of the results.
"""

import sys
import os
import time

import rlglue.RLGlue as RLGlue


class Experiment:
	""" Experiment class
	Will run a number of episodes (100 by default) and collect results
	as a cumulative average of games not lost against the number of games 
	played.
	
	The results can be collected as a string with get_result_data() """
	
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
		""" Initialize experiment """
		self.episodes = episodes
		self.results = [0] * episodes
		
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
		terminal = RLGlue.RL_episode(10)
		steps = RLGlue.RL_num_steps()
		reward = RLGlue.RL_return()
		
		#print "Episode %d\t %d steps\t reward: %d" % (episode_number, steps, reward)
		#print "Episode "+str(episode_number)+"\t "+str(totalSteps)+ " steps \t" + str(totalReward) + " total reward\t " + str(terminal) + " natural end"
	
		self.total_reward += reward
		
		# Update average
		x = self.total_reward / (self.episode_number + 1)
		self.results[self.episode_number] += (x - self.results[self.episode_number]) / self.instance
		
		self.episode_number += 1
	
	def __str__(self):
		""" Generate summary """
		return "Experiment #%d: %d/%d episodes completed. Accumulated reward: %d (%d%%)" % (self.instance, self.episode_number, self.episodes, self.total_reward, 100 * self.total_reward / self.episodes)
	
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

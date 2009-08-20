import sys

import rlglue.RLGlue as RLGlue

episode_number = 0
total_reward = 0

def runEpisode(stepLimit):
	global episode_number, total_reward
	
	terminal = RLGlue.RL_episode(stepLimit)
	steps = RLGlue.RL_num_steps()
	reward = RLGlue.RL_return()

	print "Episode %d\t %d steps\t reward: %d" % (episode_number, steps, reward)
	#print "Episode "+str(episode_number)+"\t "+str(totalSteps)+ " steps \t" + str(totalReward) + " total reward\t " + str(terminal) + " natural end"

	episode_number += 1
	total_reward += reward

taskSpec = RLGlue.RL_init()


print "\n\n----------Running a few episodes----------"
for i in xrange(100):
    runEpisode(10)
    
print "\n----------Experiment summary----------"
print "%d Episodes\t Total reward: %d" % (episode_number, total_reward)

'''
response = RLGlue.RL_agent_message("show matchboxes")
print "\n----------Experiment summary----------"
print response
'''
RLGlue.RL_cleanup()

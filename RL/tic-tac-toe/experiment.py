import sys

import rlglue.RLGlue as RLGlue

whichEpisode=0

def runEpisode(stepLimit):
	global whichEpisode
	terminal=RLGlue.RL_episode(stepLimit)
	totalSteps=RLGlue.RL_num_steps()
	totalReward=RLGlue.RL_return()

	print "Episode "+str(whichEpisode)+"\t "+str(totalSteps)+ " steps \t" + str(totalReward) + " total reward\t " + str(terminal) + " natural end"

	whichEpisode=whichEpisode+1

taskSpec = RLGlue.RL_init()


print "\n\n----------Running a few episodes----------"
runEpisode(100)
runEpisode(100)
runEpisode(100)
runEpisode(100)
runEpisode(100)
runEpisode(1)
# Remember that stepLimit of 0 means there is no limit at all!*/
runEpisode(0)
RLGlue.RL_cleanup()

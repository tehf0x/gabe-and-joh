#!/bin/bash
#
# Run experiment
#
# Usage: run_experiment.sh <agent.py> <environment.py>
# 
# For example run_experiment.sh agents/menace_agent.py environments/random_environment.py
#

if [ -z "$2" ]; then
    echo "Usage: run_experiment.sh <agent.py> <environment.py>" 1>&2
    exit 1
fi

agent="$1"
environment="$2"
experiment="experiment.py"
rl_glue="rl_glue"

#trap "echo 'Stopping children...'; ps -o pid= --ppid $$ | xargs kill" SIGINT SIGTERM

echo "Starting RL-Glue: $rl_glue"
$rl_glue &

echo "Starting environment: $environment"
python $environment > /dev/null &

echo "Starting agent: $agent"
python $agent > /dev/null &

echo "Starting experiment: $experiment"
python $experiment

echo 'Stopping...'
ps -o pid= --ppid $$ | xargs kill

#echo "Running."
#kill -TERM -$$

#read VAL

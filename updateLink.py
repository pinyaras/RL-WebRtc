#!/usr/bin/env python

# Read in a file of trace values
# and update Linux TC for each
# specified namespace or host

from __future__ import print_function

import sys
import os
import time
import json
from itertools import cycle

# check for input arg
if len(sys.argv) < 2:
    print("You must specify an input file containing trace values")
    sys.exit()

# get trace file from input arg
trace_file = sys.argv[1]

# confirm the input is a readable file
try:
    f = open(trace_file, 'r')
except OSError:
    print("Could not open file ", trace_file)
    sys.exit()

# add each line of the file to the bw_items list
# each line should contain a numeric value representing bandwidth in kb
# otherwise modify the tc command below
with open(trace_file, 'r') as inputFile:
    bw_items = [line.rstrip() for line in inputFile]

# set up cycle over bw_items
bw_cycle = cycle(bw_items)

# return the next bw element
def next_bw():
    return next(bw_cycle)

# default latency
latency = 400

# define hosts to modify
sw_lists = ['veth1','veth2']

# duration to run loop (in seconds)
seconds = 300 # 5 min test

# list of cycles in milliseconds
totalTimeMS = 5*seconds
timeout = [0.2]*totalTimeMS

# increment flag
item = 0

# for each cycle
for i in range(len(timeout)):

    # print(datetime.now().strftime('%H%M%S'))

    # get next bw value in cycle
    bw = next_bw()

    # iterate over hosts
    for s in sw_lists:
       
        # set traffic control value for host 
        # tc qdisc add dev S1-eth0 root tbf rate 1mbit burst 32kbit latency 400m
        # cmd_tbf = 'tc qdisc replace dev '+ s +' root handle 2: tbf rate '+str(bw)+'Mbit burst 15000 latency '+str(latency)+'ms'

        # traces are in kbit
        cmd_tbf = 'tc qdisc replace dev '+ s +' root handle 2: tbf rate '+str(bw)+'kbit burst 15000 latency '+str(latency)+'ms'

        # execute command
        os.system(cmd_tbf)

    # sleep (seconds)
    time.sleep(timeout[i])

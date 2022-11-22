#! /usr/bin/env python

# Compare two BWE algorithms
# and plot metrics for each

# For test purposes, the input
# files are "GCC.log" and "RL.log"

import os
import re
import sys
import glob
import fileinput
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# default observations occur in
# 200ms intervals (per config)
intervalMS = 200

# Get the file paths
def getFiles(inputPath):

	# NOTE: filenames hard coded for testing
    gccData = inputPath + "/GCC.log"
    rlData = inputPath + "/RL.log"
    files=[gccData,rlData]
    return(files)


# Extract records from the files
def parseFiles(files):

    # get file name
    # for test: file0=gcc, file1=rl
    file0 = Path(files[0]).stem
    file1 = Path(files[1]).stem

    # empty dictionary
    data = {}

	# NOTE: first pass to experiment with
	# data extraction; this step should be
	# modified to work dynamically

    # get receiving rate records
    data["rec0"] = getData("ReceivingRate",files[0])
    data["rec0File"] = file0
    data["rec1"] = getData("ReceivingRate",files[1])
    data["rec1File"] = file1

    # get delay records
    data["delay0"] = getData("Delay",files[0])
    data["delay0File"] = file0
    data["delay1"] = getData("Delay",files[1])
    data["delay1File"] = file1

    # get loss records
    data["loss0"] = getData("LossRatio",files[0])
    data["loss0File"] = file0
    data["loss1"] = getData("LossRatio",files[1])
    data["loss1File"] = file1

    # get bandwidth records
    data["bandwidth0"] = getData("BandwidthEstimate",files[0])
    data["bandwidth0File"] = file0
    data["bandwidth1"] = getData("BandwidthEstimate",files[1])
    data["bandwidth1File"] = file1

    return(data)


# Some quick text parsing to extract data
# version = {ReceivingRate, Delay, LossRatio, BandwidthEstimate}
# logFile = the file being processed
def getData(version, logFile):

	# look for colon delimited fields
    pattern = re.compile(version + ':.*')
    with open(logFile, 'r') as n:
        n = n.read()
        results = re.findall(pattern, n)
    
    # replace text
    replacePattern = version + ": "
    results = [x.replace(replacePattern,"") for x in results]
    
    # convert to int
    results = [eval(x) for x in results]
    # results = list(map(float, results))

	# treat delay values as positive
    if version =="Delay":
        results = [abs(x) for x in results]


    return(results)

# generate the graphs
def genGraphs(records):

	# Each plot is generated in a separate code block below.
	# This could be replaced by a generic plot function w/
	# child functions for each plot type; or input args from
	# user specifying which fields to extract and plot.

	####################

    # FIGURE 1: receivingRate
    plt.figure(1)
    
    # prepare plot
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # get the ranges for both sets, and the filenames
    # and plot them both
    file0rec = records["rec0"]
    file0 = records["rec0File"]
    file1rec = records["rec1"]
    file1 = records["rec1File"]

    # adjust values from kbps to Mbps
    file0rec=[x*.000001 for x in file0rec]
    file1rec=[x*.000001 for x in file1rec]

    recRange0 = range(0,len(file0rec))
    recRange1 = range(0,len(file1rec))
    
    # adjust each to stand for 200ms
    # and convert to seconds
    # (y*200)/1000
    recRangeAdj0 = [y*0.2 for y in recRange0]
    recRangeAdj1 = [y*0.2 for y in recRange1]

    # delay is x axis, range is y axis
    plt.title("Receive Rate")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Bitrate (Mbps)")
    plt.plot(recRangeAdj0, file0rec, color ="red", label=file0)
    plt.plot(recRangeAdj1, file1rec, color="blue", label=file1)
    plt.legend(loc="upper left")
    #plt.show()

    # TEMP FOR TESTING
    plt.ylim([0.0, 1.4])
    
    # store plot
    plt.savefig('RecvRate.png', bbox_inches = "tight")

	####################

    # FIGURE 2: delay
    plt.figure(2)
    
    # prepare plot
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # get the ranges for both sets, and the filenames
    # and plot them both
    file0delay = records["delay0"]
    file0 = records["delay0File"]
    file1delay = records["delay1"]
    file1 = records["delay1File"]

    delayRange0 = range(0,len(file0delay))
    delayRange1 = range(0,len(file1delay))
    
    # and adjust each to stand for 200ms
    # and convert to seconds
    delayRangeAdj0 = [y*0.2 for y in delayRange0]
    delayRangeAdj1 = [y*0.2 for y in delayRange1]
    
    # delay is x axis, ranges is y axis
    plt.title("Delay")
    plt.xlabel("Time (seconds)")
    plt.ylabel("RTT")
    plt.plot(delayRangeAdj0, file0delay, color ="red", label=file0)
    plt.plot(delayRangeAdj1, file1delay, color="blue", label=file1)
    plt.legend(loc="upper left")
    #plt.show()
    
    # store plot
    plt.savefig('Delay.png', bbox_inches = "tight")

	####################

    # FIGURE 3: loss ratio
    plt.figure(3)
    
    # prepare plot
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # get the ranges for both sets, and the filenames
    # and plot them both
    file0loss = records["loss0"]
    file0 = records["loss0File"]
    file1loss = records["loss1"]
    file1 = records["loss1File"]

    lossRange0 = range(0,len(file0loss))
    lossRange1 = range(0,len(file1loss))
    
    # and adjust each to stand for 200ms
    # and convert to seconds
    lossRangeAdj0 = [y*0.2 for y in lossRange0]
    lossRangeAdj1 = [y*0.2 for y in lossRange1]
    
    # delay is x axis, ranges is y axis
    plt.title("Packet Loss")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Loss Rate")
    plt.plot(lossRangeAdj0, file0loss, color ="red", label=file0)
    plt.plot(lossRangeAdj1, file1loss, color="blue", label=file1)
    plt.legend(loc="upper left")
    #plt.show()
    
    # store plot
    plt.savefig('Loss.png', bbox_inches = "tight")

	####################

    # FIGURE 4: Bandwidth
    plt.figure(4)
    
    # prepare plot
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # get the ranges for both sets, and the filenames
    # and plot them both
    file0bandwidth = records["bandwidth0"]
    file0 = records["bandwidth0File"]
    file1bandwidth = records["bandwidth1"]
    file1 = records["bandwidth1File"]

    # adjust values from bps to Mbps
    # gcc=0, rl=0 (in test)
    file0bandwidthAdj=[(x*.000001) for x in file0bandwidth]
    file1bandwidthAdj=[(x*.000001) for x in file1bandwidth]

    bandwidthRange0 = range(0,len(file0bandwidth))
    bandwidthRange1 = range(0,len(file1bandwidth))
    
    # and adjust each to stand for 200ms
    # and convert to seconds
    bandwidthRangeAdj0 = [y*0.2 for y in bandwidthRange0]
    bandwidthRangeAdj1 = [y*0.2 for y in bandwidthRange1]
    
    # bandwidth x axis, ranges is y axis
    plt.title("Estimated Bandwidth")
    plt.xlabel("Time (Seconds)")
    plt.ylabel("Bandwidth (Mbps)")
    plt.plot(bandwidthRangeAdj0, file0bandwidthAdj, color="red", label=file0)
    plt.plot(bandwidthRangeAdj1, file1bandwidthAdj, color="blue", label=file1)

	####################

	# Plot the Bandwidth Trace data
	# stored in "TestCapacity.txt"
    traceFile = "TestCapacity.txt"

	# get trace value records
    with open(traceFile, 'r') as inputFile:
        bw_items = [line.rstrip() for line in inputFile]

    bw_items = list(map(float, bw_items))
   
    # get the max duration between the two log files 
    traceLen = max(len(file0bandwidth), len(file1bandwidth))

	# adjust the range of trace data records to use
    traceRange = range(0,traceLen)
    traceRangeAdj = [x*0.2 for x in traceRange]

    # get the trace values corresponding to length of run
    groundTruth = bw_items[0:traceLen]

    # adjust ground truth from kb to mb
    groundTruthAdj=[x*.001 for x in groundTruth]

	# plot the trace data
    plt.plot(traceRangeAdj, groundTruthAdj, color = "black", label="Bandwidth")
    plt.legend(loc="upper left")
    #plt.show()

    # scale plot
    # plt.autoscale(enable=True, axis='both', tight=None)
    # TEMP FOR TESTING -- need to improve scaling
    plt.ylim([0.0, 2.0])
    
    # store plot
    plt.savefig('Bandwidth.png', bbox_inches = "tight")

    return


########
# MAIN #
########

# User provides a path to the log files
# being used for comparison
# `python genPlots.py [path]`

def main():

    # exit if no path given
    if len(sys.argv) == 1:
        print("Please provide a path")
        exit(1)

    # store path containing log files
    inputPath = sys.argv[1]

    # exit if path does not exist
    if not os.path.exists(inputPath):
        print("Please provide a valid path")
        exit(1)

    # get a list of files to parse
    files = getFiles(inputPath)

    # extract the data
    records = parseFiles(files)

    # generate the graphs
    genGraphs(records)

    return

if __name__ == "__main__":
    main()

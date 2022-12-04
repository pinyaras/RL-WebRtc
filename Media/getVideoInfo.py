#! /usr/bin/env python

##################################
# Extract stats from video files #
# for AlphaRTC config entries    #
##################################

# For more info see
# https://stackoverflow.com/questions/47454317/getting-video-properties-with-python-without-calling-external-software

import sys
import cv2

# get input file
videofilename = sys.argv[1]

# extract video data as cv2 object
cv2video = cv2.VideoCapture(videofilename)

# get video dimensions
height = cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT)
width  = cv2video.get(cv2.CAP_PROP_FRAME_WIDTH) 
print ("Video Dimension: height:{} width:{}".format( height, width))

# get framecount/duration/FPS
framecount     = cv2video.get(cv2.CAP_PROP_FRAME_COUNT ) 
frames_per_sec = cv2video.get(cv2.CAP_PROP_FPS)
print("Video duration (sec):", framecount / frames_per_sec)
print("Frame Count:", framecount)
print("FPS:", frames_per_sec)

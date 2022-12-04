#! /usr/bin/env python

##################################
# Conversion between mp4/yuv for #
# AlphaRTC and Monoport testing  #
##################################

# STATUS: WORK IN PROGRESS #

# TODO: convert from sys commands to ffmpeg-python
# https://github.com/kkroening/ffmpeg-python

import sys

def mp4_to_yuv():

	cmd="ffmpeg -i" + input_file + "-framerate" + fmrate + "-video_size" + resolution + "-pixel_format" + pxformat + output_file
	print(cmd) # TEST
	# TODO: execute cmd

	return


def yuv_to_mp4():

	cmd="ffmpeg -framerate" + fmrate + "-video_size" + resolution + "-pixel_format" + pxformat + "-i" + input_file + output_file
	print(cmd) # TEST
	# TODO: execute cmd


def main():


	# get input file
	# TODO: convert to argparse
	inputFile = sys.argv[1]

	# use yuv420p as standard pixel format for conversion
	# this can be modified as needed
	pxformat="yuv420p"

	# TODO: extract file type, frame rate, resolution

	# TODO: strip basename; set output filename

	# if filetype=="mp4":
		# mp4_to_yuv(input_file, fmrate, resolution, pxformat, outputfile)
	# elif filetype=="yuv":
		# yuv_to_mp4(fmrate, resolution, pxformat, input_file, outputfile)
	# else:
		# error... filetype not recognised

if __name__ == "__main__":
	main()

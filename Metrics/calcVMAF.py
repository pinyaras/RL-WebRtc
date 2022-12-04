#! /usr/bin/env python

from ffmpeg_quality_metrics import FfmpegQualityMetrics as ffqm
import matplotlib.pyplot as plt

# TODO: convert to argparse
referenceFile = sys.argv[1] # source "reference" file
processedFile = sys.argv[2] # output "processed" file

# Test to run (SNR, SSIM, VMAF, VIF)
tests=["vmaf"]

# calculate results
results = ffqm(reference, processed).calc(tests)
# print(results)

# results = dict
# results["vmaf"] = list, 1 entry for every frame
# results["vmaf"][0] = dict of outputs, including vmaf score

# get just the vmaf scores for each frame
vmafScore = results["vmaf"]
scores = [x['vmaf'] for x in vmafScore]

# plot the vmaf scores
plt.plot(scores)
plt.title('QoS: VMAF')
plt.xlabel('Frame')
plt.ylabel('Score')

# can adjust scales as needed
#plt.ylim((50,100))

# plt.show()

# scale plot
plt.autoscale(enable=True, axis='both', tight=None)

# store plot
plt.savefig('img/VMAF.png', bbox_inches = "tight")

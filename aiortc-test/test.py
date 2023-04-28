# import fractions

# import av

# codec_name = "h264_nvenc"
# MAX_FRAME_RATE = 30

# av.codec.codec.dump_codecs()

# codec = av.CodecContext.create(codec_name, "w")
# codec.width = 1920
# codec.height = 1080
# codec.bit_rate = 1000000
# codec.pix_fmt = "yuv420p"
# codec.framerate = fractions.Fraction(MAX_FRAME_RATE, 1)
# codec.time_base = fractions.Fraction(1, MAX_FRAME_RATE)
# codec.options = {
#     "profile": "baseline",
#     "level": "31",
#     "tune": "zerolatency",  # does nothing using h264_omx
# }
# codec.open()

# print(str(codec))

import math

def netowrk_util(throughput, delay, alpha=0.75):
    """
    Calculates a network utility function based on throughput and delay, with a specified alpha value for balancing.
    
    Args:
    - throughput: a float representing the network throughput in bits per second
    - delay: a float representing the network delay in seconds
    - alpha: a float representing the alpha value for balancing (default is 0.5)
    
    Returns:
    - a float representing the alpha-balanced metric
    """
    # Calculate the reciprocal of the delay in milliseconds
    rtt_ms = delay 
    rtt_reciprocal = 1 / rtt_ms
    
    # Calculate the logarithm of the throughput in bits per second
    log_throughput = math.log(throughput)
    
    # Calculate the alpha-balanced metric
    alpha_balanced_metric = alpha * log_throughput - (1 - alpha) * rtt_reciprocal
    print(alpha_balanced_metric)    
    return alpha_balanced_metric

netowrk_util(700000, 0.03)
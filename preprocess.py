import time
import numpy as np

def extract_features(connection_start_time, data_received, data_sent):
    connection_duration = time.time() - connection_start_time
    src_bytes = len(data_received)
    dst_bytes = len(data_sent)
    return np.array([connection_duration, src_bytes, dst_bytes])
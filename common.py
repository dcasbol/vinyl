from typing import Any
import numpy as np

max_diff = 2**15
ref_log = np.log1p(max_diff)
num_quant = 16
minv = -32768
maxv =  32767

def get_quantized_value(sample, previous_sample):
    diff = sample - previous_sample
    if abs(diff) > max_diff:
        diff = np.sign(diff) * max_diff
    norm_log_diff = np.sign(diff) * (np.log1p(abs(diff)) / ref_log)
    quantized_value = (norm_log_diff + 1.0) / 2.0
    quantized_value = int(num_quant * quantized_value)
    return min(quantized_value, num_quant - 1)

def get_restored_value(previous_sample, quantized_value):
    dequantized_value = (quantized_value + 0.5) / num_quant
    norm_log_diff = 2 * dequantized_value - 1.0
    restored_diff = np.sign(norm_log_diff) * np.expm1(abs(norm_log_diff) * ref_log)
    restored_value = previous_sample + round(restored_diff)
    return min(max(minv, restored_value), maxv)

class HalfBytes:
    
    def __init__(self, values=[]):
        self.values = values
        self.n = len(values) * 2

    def append(self, v):
        if self.n % 2 == 0:
            self.values.append(v)
        else:
            v0 = self.values[-1]
            self.values[-1] = v0 | (v << 4)
        self.n += 1

    def __iter__(self):
        max_i = self.n - 1
        for i in range(self.n):
            v = self[i]
            if i == max_i and v == 0:
                break
            yield v

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        v = self.values[i // 2]
        if i % 2 == 0:
            return v & 0xf
        else:
            return v >> 4
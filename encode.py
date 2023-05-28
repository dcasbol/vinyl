import wave
import struct
import numpy as np
import pickle
from common import *

# Open the WAV file
input_file = "input_audio.wav"
output_file = "compressed_audio.txt"

with wave.open(input_file, 'rb') as wav_file:
    # Get audio parameters
    sample_width = wav_file.getsampwidth()
    sample_rate = wav_file.getframerate()
    num_channels = wav_file.getnchannels()
    num_frames = wav_file.getnframes()

    assert sample_width == 2
    assert num_channels == 1
    assert sample_rate == 44100

    # Read audio data
    frames = wav_file.readframes(num_frames)

# Convert binary data to a list of samples
samples = []
for i in range(0, len(frames), sample_width):
    sample = frames[i:i+sample_width]
    value = struct.unpack('<h', sample)[0]
    samples.append(value)

# Perform compression
compressed_samples = []
previous_sample = 0

for sample in samples:
    quantized_value = get_quantized_value(sample, previous_sample)
    compressed_samples.append(quantized_value)
    previous_sample = get_restored_value(previous_sample, quantized_value)

# Write compressed samples to a text file
with open(output_file, 'w') as txt_file:
    for sample in compressed_samples:
        txt_file.write(str(sample) + '\n')

print("Compression completed. Compressed samples saved to", output_file)


import wave
import struct
import numpy as np

# Open the WAV file
input_file = "input_audio.wav"
output_file = "compressed_audio.txt"

with wave.open(input_file, 'rb') as wav_file:
    # Get audio parameters
    sample_width = wav_file.getsampwidth()
    sample_rate = wav_file.getframerate()
    num_channels = wav_file.getnchannels()
    num_frames = wav_file.getnframes()

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
max_diff = 2**14
ref_log = np.log1p(max_diff)

for sample in samples[1:]:
    diff = sample - previous_sample
    if abs(diff) > max_diff:
    	diff = max_diff * np.sign(diff)
    quantized_diff = np.sign(diff) * (np.log1p(abs(diff)) / ref_log)
    quantized_value = round(16 * ((quantized_diff + 1.0) / 2.0))
    compressed_samples.append(quantized_value)
    restored_diff = (quantized_value / 16) * 2 - 1.0
    restored_diff = np.exp(previous_sample) - 1.0
    previous_sample += restored_diff

# Write compressed samples to a text file
with open(output_file, 'w') as txt_file:
    for sample in compressed_samples:
        txt_file.write(str(sample) + '\n')

print("Compression completed. Compressed samples saved to", output_file)


import wave
import struct
import numpy as np

# Open the compressed audio file
compressed_file = "compressed_audio.txt"
decompressed_file = "decompressed_audio.wav"

with open(compressed_file, 'r') as txt_file:
    # Read the compressed samples
    compressed_samples = [int(line.strip()) for line in txt_file]

# Decompress and reconstruct the audio
sample_width = 2  # 16 bits
sample_rate = 44100  # Specify the sample rate of the original audio
num_channels = 1  # Specify the number of channels of the original audio
num_frames = len(compressed_samples)
frames = bytearray()

previous_sample = 0
max_diff = 2**14
ref_log = np.log1p(max_diff)

frames.extend(struct.pack('<h', compressed_samples[0]))  # First sample is stored as is

for quantized_value in compressed_samples[1:]:
    restored_diff = (quantized_value / 16.0) * 2 - 1.0
    diff = np.sign(restored_diff) * ref_log * np.expm1(abs(restored_diff))
    sample = previous_sample + round(diff)
    sample = max(min(sample, 32767), -32768)  # Clamp the value
    frames.extend(struct.pack('<h', sample))
    previous_sample = sample

# Write the decompressed audio to a WAV file
with wave.open(decompressed_file, 'wb') as wav_file:
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(sample_rate)
    wav_file.setnchannels(num_channels)
    wav_file.writeframes(frames)

print("Decompression completed. Decompressed audio saved to", decompressed_file)


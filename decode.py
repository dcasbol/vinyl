import wave
import struct
import numpy as np
from common import *

# Open the compressed audio file
compressed_file = "compressed_audio.npz"
decompressed_file = "decompressed_audio.wav"

compressed_samples = np.load(compressed_file)["a"]
compressed_samples = HalfBytes(compressed_samples)

# Decompress and reconstruct the audio
sample_width = 2  # 16 bits
sample_rate = 44100  # Specify the sample rate of the original audio
num_channels = 1  # Specify the number of channels of the original audio
frames = bytearray()

previous_sample = 0

for quantized_value in compressed_samples:
    previous_sample = get_restored_value(previous_sample, quantized_value)
    frames.extend(struct.pack('<h', previous_sample))

# Write the decompressed audio to a WAV file
with wave.open(decompressed_file, 'wb') as wav_file:
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(sample_rate)
    wav_file.setnchannels(num_channels)
    wav_file.writeframes(frames)

print("Decompression completed. Decompressed audio saved to", decompressed_file)


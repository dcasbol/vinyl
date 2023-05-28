# vinyl
A simple lossy codec. Just for fun. Based on the idea that audio waves rarely change abruptly and those changes are often minor. So far it works and achieves compression rate of 5x without significant noise.

## To do next
1. Use terminal arguments for input/output files.
2. Adapt to frequency, number of channels and sample size.
3. Currently using log-scale for quantization. Compute optimal scale from histogram.
4. Use jit compilation (e.g. numba)
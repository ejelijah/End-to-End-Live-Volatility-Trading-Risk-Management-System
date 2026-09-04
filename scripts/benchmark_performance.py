import time
import numpy as np
import sys
import os
sys.path.append(os.path.abspath("build"))
import quant_core
from core.python.models.sabr import SABRModel # Your Python version

# Setup
alpha, beta, rho, volvol = 0.2, 0.5, -0.5, 0.3
F, K, T = 228.5, 235.0, 1/365
iterations = 10000


# 1. Benchmark Python
py_model = SABRModel(alpha, beta, rho, volvol)
start_py = time.time()
for _ in range(iterations):
    _ = py_model.lognormal_vol(F, K, T)
end_py = time.time()

# 2. Benchmark C++
cpp_engine = quant_core.SABREngine(alpha, beta, rho, volvol)
start_cpp = time.time()
for _ in range(iterations):
    _ = cpp_engine.get_implied_vol(F, K, T)
end_cpp = time.time()

py_time = (end_py - start_py) / iterations * 1e6 # microseconds
cpp_time = (end_cpp - start_cpp) / iterations * 1e6 # microseconds

print(f"--- LATENCY BENCHMARK ({iterations} iterations) ---")
print(f"Python Avg Latency: {py_time:.2f} μs")
print(f"C++ Avg Latency:    {cpp_time:.2f} μs")
print(f"Speedup Factor:     {py_time / cpp_time:.1f}x")

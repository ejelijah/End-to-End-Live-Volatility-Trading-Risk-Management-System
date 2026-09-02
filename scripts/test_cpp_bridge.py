import sys
import os

# 1. Point Python to the 'build' folder so it can find 'quant_core'
# This is the "Bridge" connecting your C++ binary to your Python script
sys.path.append(os.path.abspath("build"))

try:
    import quant_core
    print("✅ SUCCESS: quant_core imported successfully!")
except ImportError as e:
    print(f"❌ ERROR: Could not import quant_core. {e}")
    sys.exit(1)

# 2. Initialize the C++ Engine
# Parameters: alpha, beta, rho, volvol
# We use the same 'Initial Guess' from our research phase
alpha, beta, rho, volvol = 0.2, 0.5, -0.5, 0.3
engine = quant_core.SABREngine(alpha, beta, rho, volvol)

# 3. Define Market Parameters
F = 228.50  # Forward Price
K = 235.00  # Strike Price
T = 1/365   # 1 Day to Maturity

# 4. The High-Speed Calculation
# This call goes through the bridge, into the C++ kitchen, and back
cpp_vol = engine.get_implied_vol(F, K, T)

print("\n--- QUANT BRIDGE RESULTS FOR ELIJAH EJ ---")
print(f"Target Strike:   USD {K}")
print(f"C++ Calculated Vol: {cpp_vol:.6f}")
print("------------------------------------------")
print("Status: C++ Math is now accessible in Python.")

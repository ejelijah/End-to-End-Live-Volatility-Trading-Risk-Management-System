import sys
import os
import numpy as np

# 1. Point to the build folder to find your compiled C++ module
sys.path.append(os.path.abspath("build"))

try:
    import quant_core
    print("✅ C++ Risk Engine Linked Successfully!")
except ImportError:
    print("❌ Link failed. Check if quant_core.so exists in the build folder.")
    sys.exit(1)

# 2. Initialize the Engine with your Calibrated SABR parameters
# (Using the Alpha, Rho, and Vol-of-Vol we found earlier)
alpha, beta, rho, volvol = 0.20, 0.5, -0.50, 0.30
engine = quant_core.SABREngine(alpha, beta, rho, volvol)

# 3. Define a "Live" Scenario
S = 228.50    # Current AAPL Price
K = 230.00    # Strike Price
T = 30 / 365  # 30 days to expiry
r = 0.05      # 5% Interest rate

# Use your C++ engine to get the Implied Vol for this strike
sigma = engine.get_implied_vol(S, K, T)

# 4. Calculate DELTA using the C++ Risk Layer
delta = engine.get_delta(S, K, T, r, sigma)

print("\n--- LIVE RISK ANALYSIS ---")
print(f"Asset:           AAPL")
print(f"Spot Price:      USD {S}")
print(f"SABR Volatility: {sigma:.4f}")
print(f"Option Delta:    {delta:.4f}")

# 5. The "Risk Management" Logic
shares_to_hedge = -int(delta * 100) # For 1 option contract (100 shares)
print(f"\nACTION: To remain Delta-Neutral, sell {abs(shares_to_hedge)} shares of AAPL.")
print("--------------------------")

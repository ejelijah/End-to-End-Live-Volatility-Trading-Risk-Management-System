import sys
import os
import pandas as pd
import numpy as np

# Point to build folder
sys.path.append(os.path.abspath("build"))
import quant_core

# 1. Setup the Engine & Risk Manager
# Parameters from our calibration
alpha, beta, rho, volvol = 0.20, 0.5, -0.50, 0.30
engine = quant_core.SABREngine(alpha, beta, rho, volvol)
risk_manager = quant_core.RiskController(10000.0, 5000.0)

# 2. Load Real Market Data
df = pd.read_csv("data/raw/AAPL_2026-09-02_options.csv")
S = 228.50 # Spot Price
r = 0.05   # Interest Rate
T = 30/365 # 30 Days

print(f"--- STARTING LIVE SIMULATION FOR {len(df)} STRIKES ---")

current_pnl = 0.0

for i, row in df.iterrows():
    K = row['strike']
    
    # A. Calculate Implied Vol in C++
    sigma = engine.get_implied_vol(S, K, T)
    
    # B. Calculate Delta in C++
    delta = engine.get_delta(S, K, T, r, sigma)
    
    # C. Check Risk in C++
    # We simulate a "Blow-up" at Strike #25
    if i == 25:
        current_pnl = -15000.0 # Force a crash
        print("\n[!!!] FLASH CRASH DETECTED [!!!]")

    if risk_manager.is_trade_allowed(current_pnl, delta * 100):
        print(f"Strike {K:.1f} | Vol: {sigma:.4f} | Delta: {delta:.4f} | STATUS: TRADE EXECUTED")
    else:
        print(f"Strike {K:.1f} | Delta: {delta:.4f} | STATUS: REJECTED (RISK LIMIT EXCEEDED)")
        if i > 25:
            print(">>> SYSTEM LOCKED BY C++ KILL SWITCH <<<")
            break

print("\n--- SIMULATION COMPLETE ---")

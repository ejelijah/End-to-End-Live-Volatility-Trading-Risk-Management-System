import pandas as pd
import numpy as np
import datetime
from core.python.pricing_engine import BlackScholesEngine
from core.python.calibrator import VolatilityCalibrator

# 1. Load your new data
# Replace with your actual filename from the terminal output
CSV_PATH = "data/raw/AAPL_2026-09-02_options.csv"
df = pd.read_csv(CSV_PATH)

# Market Parameters
S = df.iloc[(df['strike']-228).abs().argsort()[:1]]['strike'].values[0]
print(f"Using Forward Price: USD {S}")
r = 0.05   # Fed Funds Rate (~5%)
T = 1 / 365 # 1 day to maturity

# 2. Calculate Market Implied Volatilities
market_vols = []
strikes = []

print("Calculating Market Implied Volatilities...")
for index, row in df.iterrows():
    engine = BlackScholesEngine(S, row['strike'], T, r, 0.5)
    iv = engine.find_implied_vol(row['mid_price'])
    market_vols.append(iv)
    strikes.append(row['strike'])

# 3. Calibrate SABR
print("Calibrating SABR Model to Market Data...")
calibrator = VolatilityCalibrator(S, strikes, np.array(market_vols), T)
alpha, rho, volvol = calibrator.calibrate()

print("\n--- CALIBRATION RESULTS FOR ELIJAH EJ ---")
print(f"Alpha (At-the-money Vol): {alpha:.4f}")
print(f"Rho (Correlation):        {rho:.4f}")
print(f"Vol-of-Vol:               {volvol:.4f}")

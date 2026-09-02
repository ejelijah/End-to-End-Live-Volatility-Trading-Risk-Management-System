import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from core.python.models.sabr import SABRModel

# 1. Load the data you just calibrated
CSV_PATH = "data/raw/AAPL_2026-09-02_options.csv"
df = pd.read_csv(CSV_PATH)

# Use the results you just got (The initial guesses)
alpha, rho, volvol = 0.2, -0.5, 0.3
S = 228.50 # Ensure this matches your calibration script
T = 1/365

# 2. Generate the Model Curve
sabr = SABRModel(alpha, 0.5, rho, volvol)
strike_range = np.linspace(df['strike'].min(), df['strike'].max(), 100)
model_vols = [sabr.lognormal_vol(S, k, T) for k in strike_range]

# 3. Plot
plt.figure(figsize=(10, 6))
# We don't have the market IVs saved yet, so let's just look at the model shape
plt.plot(strike_range, model_vols, label="SABR Model (Initial Guess)", color='red', linestyle='--')
plt.title(f"AAPL Volatility Smile - {S} Forward")
plt.xlabel("Strike Price")
plt.ylabel("Implied Volatility")
plt.legend()
plt.grid(True)
plt.show()

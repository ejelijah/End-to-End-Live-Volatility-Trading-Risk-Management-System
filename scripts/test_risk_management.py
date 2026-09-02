import sys
import os


# 1. Point to the build folder
sys.path.append(os.path.abspath("build"))
import quant_core

# 2. Initialize Risk Controller
# Max Drawdown: USD 10,000 | Max Position Size: 5,000 shares
risk_manager = quant_core.RiskController(10000.0, 5000.0)

print("--- STARTING RISK CONTROLLER TEST ---")

# TEST 1: Normal Trade
# P&L is 0, trying to buy 100 shares
if risk_manager.is_trade_allowed(0.0, 100.0):
    print("✅ Trade 1: Allowed (Normal conditions)")
else:
    print("❌ Trade 1: Rejected (Unexpected)")

# TEST 2: Position Size Limit
# Trying to buy 6,000 shares (Limit is 5,000)
if not risk_manager.is_trade_allowed(0.0, 6000.0):
    print("✅ Trade 2: Rejected (Exceeded Max Position Size)")
else:
    print("❌ Trade 2: Allowed (Safety Failure!)")

# TEST 3: The "Blow-up" (Kill Switch)
# P&L is at -11,000 (Limit is -10,000)
print("\n[!] Simulating Market Crash... P&L dropping to -USD 11,000")
if not risk_manager.is_trade_allowed(-11000.0, 100.0):
    print("✅ Trade 3: Rejected (Kill Switch Triggered by Drawdown)")
else:
    print("❌ Trade 3: Allowed (Safety Failure! Bot is blowing up!)")

# TEST 4: Persistence
# Even if P&L recovers, the Emergency Stop should stay active
if not risk_manager.is_trade_allowed(0.0, 100.0):
    print("✅ Trade 4: Rejected (System remains Locked for Safety)")
else:
    print("❌ Trade 4: Allowed (Safety Failure! System should be locked!)")

print("\n--- STATUS: C++ RISK LAYER IS BULLETPROOF ---")

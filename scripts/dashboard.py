import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sys
import os

# 1. Link to your C++ Engine
sys.path.append(os.path.abspath("build"))
import quant_core

st.set_page_config(page_title="NeuralQuant: Volatility Cockpit", layout="wide")

st.title("Live Volatility & Risk Dashboard")
st.markdown("---")

# --- SIDEBAR: SYSTEM CONTROLS ---
st.sidebar.header("🕹️ Model Parameters (SABR)")
alpha = st.sidebar.slider("Alpha (ATM Vol)", 0.01, 1.0, 0.20)
rho = st.sidebar.slider("Rho (Skew)", -0.99, 0.99, -0.50)
volvol = st.sidebar.slider("Vol-of-Vol", 0.01, 1.0, 0.30)
beta = 0.5 # Fixed for equities

st.sidebar.header("🛡️ Risk Limits")
max_loss = st.sidebar.number_input("Max Drawdown (USD)", value=10000)
max_pos = st.sidebar.number_input("Max Position Size", value=5000)

# Initialize C++ Objects
engine = quant_core.SABREngine(alpha, beta, rho, volvol)
risk_controller = quant_core.RiskController(float(max_loss), float(max_pos))

# --- MAIN PANEL: LIVE MARKET SIM ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Volatility Smile (C++ Engine)")
    
    # Generate Strike Range
    S = st.number_input("Current Stock Price (S)", value=228.50)
    T = st.slider("Time to Expiry (Days)", 1, 365, 30) / 365
    
    strikes = np.linspace(S*0.8, S*1.2, 50)
    vols = [engine.get_implied_vol(S, k, T) for k in strikes]
    
    # Plotly Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strikes, y=vols, mode='lines', name='SABR Smile', line=dict(color='#00ffcc', width=3)))
    fig.update_layout(template="plotly_dark", xaxis_title="Strike Price", yaxis_title="Implied Volatility")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🛡️ Real-Time Risk")
    
    target_k = st.number_input("Target Strike for Trade", value=230.0)
    r = 0.05
    
    # Calculate Metrics in C++
    sigma = engine.get_implied_vol(S, target_k, T)
    delta = engine.get_delta(S, target_k, T, r, sigma)
    
    # Display Metrics
    st.metric("SABR Volatility", f"{sigma:.4f}")
    st.metric("Option Delta", f"{delta:.4f}")
    
    # Kill Switch Status
    current_pnl = st.number_input("Simulated Current P&L", value=0.0)
    is_allowed = risk_controller.is_trade_allowed(current_pnl, delta * 100)
    
    if is_allowed:
        st.success("✅ SYSTEM STATUS: NOMINAL")
        st.info(f"Hedge Action: Sell {int(delta*100)} shares")
    else:
        st.error("🚨 SYSTEM STATUS: LOCKED (RISK BREACH)")
        st.warning("C++ Kill Switch Active. Emergency Stop engaged.")

# --- FOOTER: PERFORMANCE ---
st.markdown("---")
st.caption("Engine Core: C++17 | Interface: Python 3.13 | Latency: < 2μs per calculation")

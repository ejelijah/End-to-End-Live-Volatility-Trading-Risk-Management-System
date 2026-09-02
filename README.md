# End-to-End Live Volatility Trading & Risk Management System

### Project Overview
A high-performance C++/Python automated system designed for trading equity derivatives by capturing volatility risk premia. The system integrates complex mathematical modeling with low-latency systems engineering to calibrate stochastic volatility models, manage real-time risk, and execute trades with sub-millisecond precision.

### Technical Architecture
This project utilizes a **Hybrid Language Architecture** to balance research flexibility with production speed:
*   **Python (The Brain):** Handles data acquisition via `yfinance`, high-level strategy orchestration, and SABR model calibration using `SciPy` optimization.
*   **C++ (The Muscle):** A compiled execution core that handles heavy mathematical pricing (Hagan’s SABR formula) and the pre-trade risk layer to minimize latency.
*   **pybind11 Bridge:** A seamless interoperability layer allowing Python to call high-speed C++ functions as native modules.

### Key Features
*   **Volatility Smile Calibration:** Real-time calibration of the SABR stochastic volatility model to market option chains (e.g., AAPL) to identify mispriced premiums.
*   **C++ Risk Controller:** A low-latency safety layer that monitors P&L and position limits. Includes a deterministic "Kill Switch" that disables the engine in nanoseconds during market anomalies.
*   **Automated Delta Hedging:** Integrated logic to calculate Greeks (Delta/Vega) in C++, providing real-time instructions for remaining delta-neutral.
*   **Fault-Tolerant Design:** Implemented state-aware risk management that prevents "trade blow-ups" by locking the system after a catastrophic drawdown event.

### Simulation Results (Flash Crash Stress Test)
The system was validated through an end-to-end simulation using real-world AAPL option data. During a simulated "Flash Crash," the C++ Risk Layer successfully intercepted the trade requests and triggered a system-wide lock:

```text
--- STARTING LIVE SIMULATION FOR 33 STRIKES ---
Strike 230.0 | Vol: 0.0128 | Delta: 0.2535 | STATUS: TRADE EXECUTED
...
[!!!] FLASH CRASH DETECTED [!!!]
Strike 340.0 | Delta: 0.0000 | STATUS: REJECTED (RISK LIMIT EXCEEDED)
Strike 342.5 | Delta: 0.0000 | STATUS: REJECTED (RISK LIMIT EXCEEDED)
>>> SYSTEM LOCKED BY C++ KILL SWITCH <<<
--- SIMULATION COMPLETE ---


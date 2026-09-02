import numpy as np
from scipy.stats import norm

class BlackScholesEngine:
    def __init__(self, S, K, T, r, sigma):
        self.S = S          # Current Stock Price
        self.K = K          # Strike Price
        self.T = T          # Time to Maturity (Years)
        self.r = r          # Risk-free Rate
        self.sigma = sigma  # Implied Volatility

    def get_greeks(self):
        """Calculates Delta, Gamma, Vega, Theta, and Rho."""
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        
        # Delta
        delta = norm.cdf(d1)
        
        # Gamma
        gamma = norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))
        
        # Vega (Sensitivity to Volatility) - THIS IS THE MOST IMPORTANT FOR US
        vega = self.S * norm.pdf(d1) * np.sqrt(self.T)
        
        return {"delta": delta, "gamma": gamma, "vega": vega}

    def price_call(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
    
    def find_implied_vol(self, market_price, iterations=100, precision=1.0e-5):
        """Finds the implied volatility using the Newton-Raphson method."""
    # Initial guess
        sigma = 0.5
        for i in range(iterations):
            self.sigma = sigma
            price = self.price_call()
            diff = market_price - price
            if abs(diff) < precision:
                return sigma
            
        # Use Vega as the derivative for Newton-Raphson
            vega = self.get_greeks()['vega']
            if vega == 0: break # Avoid division by zero
        
        sigma = sigma + diff / vega
        return sigma


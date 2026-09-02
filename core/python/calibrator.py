import numpy as np
from scipy.optimize import minimize
from core.python.models.sabr import SABRModel # Assuming you moved your SABR code here

class VolatilityCalibrator:
    def __init__(self, forward, strikes, market_vols, expiry):
        self.F = forward
        self.K = strikes
        self.market_vols = market_vols
        self.T = expiry

    def cost_function(self, params):
        alpha, rho, volvol = params
        # Beta is usually fixed at 0.5 for equity
        sabr = SABRModel(alpha, 0.5, rho, volvol)
        
        model_vols = []
        for k in self.K:
            model_vols.append(sabr.lognormal_vol(self.F, k, self.T))
            
        # We want the Sum of Squared Errors to be zero
        return np.sum((np.array(model_vols) - self.market_vols)**2)

    def calibrate(self):
        # Initial guesses: [alpha, rho, volvol]
        initial_guess = [0.2, -0.5, 0.3]
        
        # Constraints: rho must be between -1 and 1
        bounds = [(0.001, None), (-0.999, 0.999), (0.001, None)]
        
        result = minimize(self.cost_function, initial_guess, bounds=bounds)
        return result.x # Returns [alpha, rho, volvol]
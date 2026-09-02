import numpy as np

class SABRModel:
    def __init__(self, alpha, beta, rho, volvol):
        self.alpha = alpha  # Initial Volatility
        self.beta = beta    # Elasticity (usually 0.5 for equities)
        self.rho = rho      # Correlation between price and vol
        self.volvol = volvol # Volatility of Volatility

    def lognormal_vol(self, F, K, T):
        """Calculates the SABR Implied Volatility for a given Strike (K)."""
        # This is the 'Hagan Formula' - the industry standard
        if F == K: # At-the-money case
            return self.alpha / (F**(1 - self.beta))
        
        logFK = np.log(F / K)
        FK_beta = (F * K)**((1 - self.beta) / 2)
        z = (self.volvol / self.alpha) * FK_beta * logFK
        chi_z = np.log((np.sqrt(1 - 2*self.rho*z + z**2) + z - self.rho) / (1 - self.rho))
        
        # The core SABR formula
        numerator = self.alpha * (1 + (((1 - self.beta)**2 / 24) * (self.alpha**2 / (FK_beta**2)) + 
                    (1/4) * (self.rho * self.beta * self.volvol * self.alpha / FK_beta) + 
                    ((2 - 3 * self.rho**2) / 24) * self.volvol**2) * T)
        denominator = FK_beta * (1 + ((1 - self.beta)**2 / 24) * logFK**2 + ((1 - self.beta)**4 / 1920) * logFK**4)
        
        return (numerator / denominator) * (z / chi_z)
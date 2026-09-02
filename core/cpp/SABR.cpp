#include "SABR.h"

SABREngine::SABREngine(double alpha, double beta, double rho, double volvol)
    : alpha_(alpha), beta_(beta), rho_(rho), volvol_(volvol) {}

double SABREngine::get_implied_vol(double F, double K, double T) {
    if (std::abs(F - K) < 1e-8) {
        return alpha_ / std::pow(F, 1.0 - beta_);
    }

    double logFK = std::log(F / K);
    double FK_beta = std::pow(F * K, (1.0 - beta_) / 2.0);
    double z = (volvol_ / alpha_) * FK_beta * logFK;
    double chi_z = std::log((std::sqrt(1.0 - 2.0 * rho_ * z + z * z) + z - rho_) / (1.0 - rho_));

    double numerator = alpha_ * (1.0 + (
        (std::pow(1.0 - beta_, 2.0) / 24.0) * (alpha_ * alpha_ / (FK_beta * FK_beta)) +
        (0.25 * rho_ * beta_ * volvol_ * alpha_ / FK_beta) +
        ((2.0 - 3.0 * rho_ * rho_) / 24.0) * volvol_ * volvol_
    ) * T);

    double denominator = FK_beta * (1.0 + (std::pow(1.0 - beta_, 2.0) / 24.0) * logFK * logFK + 
                         (std::pow(1.0 - beta_, 4.0) / 1920.0) * std::pow(logFK, 4.0));

    return (numerator / denominator) * (z / chi_z);
}

double SABREngine::get_delta(double S, double K, double T, double r, double sigma) {
    // Safety check to avoid division by zero or NaN
    if (sigma <= 0 || T <= 0) return 0.0;
    
    double d1 = (std::log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * std::sqrt(T));
    return 0.5 * (1.0 + std::erf(d1 / std::sqrt(2.0))); // Standard Normal CDF
}
RiskController::RiskController(double max_drawdown, double max_position_size)
    : max_drawdown_(max_drawdown), max_position_size_(max_position_size) {}

bool RiskController::is_trade_allowed(double current_pnl, double proposed_size) {
    if (emergency_stop_active_) return false;
    
    // 1. Drawdown Check: If we've lost more than our limit, kill the bot
    if (current_pnl < -max_drawdown_) {
        trigger_emergency_stop();
        return false;
    }
    
    // 2. Position Limit Check
    if (std::abs(proposed_size) > max_position_size_) return false;

    return true;
}

void RiskController::trigger_emergency_stop() {
    emergency_stop_active_ = true;
    // In a real system, this would also send a "Cancel All" signal to the exchange
}

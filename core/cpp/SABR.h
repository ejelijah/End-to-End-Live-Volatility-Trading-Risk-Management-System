#ifndef SABR_H
#define SABR_H

#include <cmath>
#include <algorithm>

class SABREngine {
public:
    SABREngine(double alpha, double beta, double rho, double volvol);
    double get_implied_vol(double F, double K, double T);
    
    // THIS LINE MUST BE HERE:
    double get_delta(double S, double K, double T, double r, double sigma);

private:
    double alpha_, beta_, rho_, volvol_;
};

class RiskController {
    public:
        RiskController(double max_drawdown, double max_position_size);
        
        // Checks if a trade is allowed based on current risk
        bool is_trade_allowed(double current_pnl, double proposed_size);
        
        // The "Kill Switch"
        void trigger_emergency_stop();
    
    private:
        double max_drawdown_;
        double max_position_size_;
        bool emergency_stop_active_ = false;
    };
    

#endif

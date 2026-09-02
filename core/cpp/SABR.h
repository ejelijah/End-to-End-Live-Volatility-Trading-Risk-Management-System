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

#endif

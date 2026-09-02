#include <iostream>
#include "SABR.h"

int main() {
    // Initializing with the same "Initial Guess" numbers
    SABREngine engine(0.2, 0.5, -0.5, 0.3);
    
    double F = 228.50;
    double K = 230.00;
    double T = 0.01; // 1% of a year
    
    double vol = engine.get_implied_vol(F, K, T);
    
    std::cout << "--- C++ ENGINE TEST ---" << std::endl;
    std::cout << "Strike: " << K << " | Implied Vol: " << vol << std::endl;
    
    return 0;
}

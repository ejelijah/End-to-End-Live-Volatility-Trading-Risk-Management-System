#include <pybind11/pybind11.h>
#include "SABR.h"

namespace py = pybind11;

PYBIND11_MODULE(quant_core, m) {
    m.doc() = "High-performance Quant Engine for Volatility Trading";

    py::class_<SABREngine>(m, "SABREngine")
        .def(py::init<double, double, double, double>())
        .def("get_implied_vol", &SABREngine::get_implied_vol, 
             "Calculates SABR Implied Volatility",
             py::arg("F"), py::arg("K"), py::arg("T"))
        .def("get_delta", &SABREngine::get_delta, 
             "Calculates Option Delta",
             py::arg("S"), py::arg("K"), py::arg("T"), py::arg("r"), py::arg("sigma"));
            
             py::class_<RiskController>(m, "RiskController")
    .def(py::init<double, double>())
    .def("is_trade_allowed", &RiskController::is_trade_allowed)
    .def("trigger_emergency_stop", &RiskController::trigger_emergency_stop);

}



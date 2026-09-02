cmake_minimum_required(VERSION 3.10)
project(QuantEngine)

set(CMAKE_CXX_STANDARD 17)

# 1. Find Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# 2. Ask Python where pybind11 is installed
execute_process(
    COMMAND "${Python3_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# 3. Load pybind11 using the path we just found
find_package(pybind11 REQUIRED PATHS ${pybind11_DIR})

# 4. Build the module
pybind11_add_module(quant_core core/cpp/python_bridge.cpp core/cpp/SABR.cpp)

# 5. Link Python libraries (Crucial for macOS)
target_link_libraries(quant_core PRIVATE Python3::Python)



cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)

project(OBC_CPP)

# Initialize the SDK
pico_sdk_init()

# Define source files
file(GLOB_RECURSE SRC_FILES
    "*.cpp"
)

# Build the executable
add_executable(obc_cpp ${SRC_FILES})

# Link libraries
target_link_libraries(obc_cpp pico_stdlib pico_multicore hardware_adc hardware_spi)

# Enable USB output (optional)
pico_enable_stdio_usb(obc_cpp 1)
pico_enable_stdio_uart(obc_cpp 0)

# Generate .uf2, .bin, .elf
pico_add_extra_outputs(obc_cpp)

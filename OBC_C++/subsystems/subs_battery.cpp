// subs_battery.cpp



// ++++++++++++++ Imports/Installs ++++++++++++++ //
#include "pico/stdlib.h"



// ++++++++++++++ Class Definition ++++++++++++++ //
class Battery {
    private:
        int port_input;
        int port_output;
        
    public:
        Battery() {
            port_input = config.PORT_BATTERY_INPUT;
            port_output = config.PORT_BATTERY_OUTPUT;
        }
};
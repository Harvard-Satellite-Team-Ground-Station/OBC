// data_battery.cpp


// ++++++++++++++ Imports/Installs ++++++++++++++ //
#include <iostream>
#include <random>
#include <thread>
#include <chrono>
#include <string>
#define DATA_OUTPUT_PADDING 40


// ++++++++++++++ Helper Functions ++++++++++++++ //
void generate_battery_data() {
    // Random number generation setup for battery voltage between 35000 and 41000 mV
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(35000, 41000);
    // Simulate the battery voltage
    int v_bat = dist(gen);
    // Calculate battery percentage based on voltage
    int battery_percentage = 100 * (v_bat - 35000) / 6000;
    // For testing purposes, you can override with a random percentage
    battery_percentage = rand() % 101; // Random value between 0 and 100
    // Output formatting with padding
    std::string output_part1 = "[DATA_BATTERY_BP]";
    int padding_length = DATA_OUTPUT_PADDING - output_part1.length();
    std::string padding(padding_length, ' '); // Create padding string
    // Output the formatted result
    std::cout << output_part1 << padding << "[" << battery_percentage << "]" << std::endl;
}


// ++++++++++++++ Main Function ++++++++++++++ //
int main() {
    while (true) {
        // Interval to run measurements on
        std::this_thread::sleep_for(std::chrono::seconds(1));
        // Generate and print battery data
        generate_battery_data();
    }
    return 0;
}

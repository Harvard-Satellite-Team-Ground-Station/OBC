// scheduler.cpp


// ++++++++++++++ Imports/Installs ++++++++++++++ //
#include <iostream>
#include <vector>
#include <thread>
#include <chrono>
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <unordered_map>
#include <string>
#include <queue>
#include <regex>


// ++++++++++++++ Class Definition ++++++++++++++ //
class Scheduler {
public:
    Scheduler()
        : current_state("bootup"), checkpoint(false), deployed_already(false) {}

    void start_process(int process_id, const std::string& process_type) {
        std::cout << "Starting process " << process_id << " of type " << process_type << std::endl;
        // Here you would spawn a thread or process, but we'll simulate with threads
        std::thread process_thread(&Scheduler::run_script, this, process_id, process_type);
        process_thread.detach();  // Detach the thread to simulate an independent process
    }

    void stop_process(int process_id) {
        std::cout << "Stopping process " << process_id << std::endl;
        // In a real system, you'd stop the actual process
    }

    void update_state(const std::string& state) {
        current_state = state;
        std::cout << "State updated to: " << current_state << std::endl;
    }

    void run_scheduler() {
        // Simulate the data process queue
        std::queue<std::string> output_queue;
        // Start the bootup state process
        start_process(100, "bootup");

        // Main state transition loop
        while (true) {
            std::this_thread::sleep_for(std::chrono::milliseconds(500));  // Simulate wait

            // Check if a new output is available (you would likely do this based on process output)
            if (!output_queue.empty()) {
                std::string output = output_queue.front();
                output_queue.pop();
                std::cout << output << std::endl; // Process output
                
                // Here you would extract data from the output (like in Python code)
                handle_state_transition(output);
            }
        }
    }

private:
    std::string current_state;
    bool checkpoint;
    bool deployed_already;

    // Simulate running a script
    void run_script(int process_id, const std::string& process_type) {
        std::this_thread::sleep_for(std::chrono::seconds(2));  // Simulate process running
        std::string output = "[DATA] Some output from process " + std::to_string(process_id);
        std::cout << output << std::endl;
    }

    // Handle state transition based on process output
    void handle_state_transition(const std::string& output) {
        if (current_state == "bootup") {
            if (output.find("[STATE_BOOTUP] [Ended]") != std::string::npos) {
                current_state = "detumble";
                start_process(101, "detumble");
            }
        } else if (current_state == "detumble") {
            if (output.find("DATA_IMU_AV") != std::string::npos) {
                if (extract_data(output) <= 0) {
                    current_state = "charge";
                    stop_process(101);
                    start_process(102, "charge");
                }
            }
        } else if (current_state == "charge") {
            if (output.find("DATA_BATTERY_BP") != std::string::npos) {
                if (extract_data(output) >= 75) {
                    current_state = "antennas";
                    stop_process(102);
                    start_process(103, "antennas");
                }
            }
        } else if (current_state == "antennas") {
            if (output.find("DATA_BATTERY_BP") != std::string::npos) {
                if (extract_data(output) >= 50) {
                    checkpoint = true;
                }
            }

            if (checkpoint && output.find("DATA_STARTRACKER_POS") != std::string::npos) {
                auto values = extract_data_multiple(output);
                if (values[0] > 90 && values[1] > 90 && values[2] > 90) {
                    checkpoint = false;
                    current_state = "comms";
                    stop_process(103);
                    start_process(104, "comms");
                }
            }
        } else if (current_state == "comms") {
            if (output.find("DATA_BATTERY_BP") != std::string::npos) {
                if (extract_data(output) >= 50) {
                    checkpoint = true;
                }
            }
            if (checkpoint && output.find("DATA_IMU_AV") != std::string::npos) {
                if (extract_data(output) <= 1) {
                    checkpoint = false;
                    stop_process(104);
                    if (!deployed_already) {
                        deployed_already = true;
                        current_state = "deploy";
                        start_process(105, "deploy");
                    } else {
                        current_state = "orient";
                        start_process(106, "orient");
                    }
                }
            }
        } else if (current_state == "deploy") {
            if (output.find("DATA_BATTERY_BP") != std::string::npos) {
                if (extract_data(output) >= 30) {
                    current_state = "orient";
                    stop_process(105);
                    start_process(106, "orient");
                }
            }
        } else if (current_state == "orient") {
            if (output.find("DATA_STARTRACKER_POS") != std::string::npos) {
                auto values = extract_data_multiple(output);
                if (values[0] > 90 && values[1] > 90 && values[2] > 90) {
                    stop_process(106);
                    current_state = "comms";
                    start_process(104, "comms");
                }
            }
        }
    }

    // Helper function to extract single data from output
    int extract_data(const std::string& output) {
        std::regex rgx(R"(\[([-+]?\d+)\])");
        std::smatch match;
        if (std::regex_search(output, match, rgx)) {
            return std::stoi(match[1].str());
        }
        return 0;  // Return default if no data found
    }

    // Helper function to extract multiple data points
    std::vector<int> extract_data_multiple(const std::string& output) {
        std::regex rgx(R"(\[([-+]?\d+(?:,\s*[-+]?\d+)*)\])");
        std::smatch match;
        std::vector<int> values;
        if (std::regex_search(output, match, rgx)) {
            std::string data_str = match[1].str();
            std::stringstream ss(data_str);
            std::string temp;
            while (std::getline(ss, temp, ',')) {
                values.push_back(std::stoi(temp));
            }
        }
        return values;
    }
};


// ++++++++++++++++ Main Function ++++++++++++++++ //
int main() {
    Scheduler scheduler;
    std::thread scheduler_thread(&Scheduler::run_scheduler, &scheduler);
    
    // Join the scheduler thread to main
    scheduler_thread.join();
    return 0;
}


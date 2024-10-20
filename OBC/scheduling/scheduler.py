# ///////////////////////////////////////////////////////////////// #
# DONE step 1: run a process
# DONE step 2: run a process with real-time print updates
# DONE step 3: accomplish this with two or more programs
# DONE step 4: kill a program mid-run
# WORKING step 5: dynamically start up a process
# ///////////////////////////////////////////////////////////////// #


# IMPORTS
import multiprocessing
import subprocess
import queue
import os
import re


# VARIABLES
scheduling_dir = os.path.dirname(os.path.abspath(__file__))
data_processes = [ # insert relative paths to these files
    scheduling_dir + "/data_processes/battery_data.py",            # data process id = 2
    scheduling_dir + "/data_processes/imu_data.py",                # data process id = 1
]
state_processes = [ # insert relative paths to these files
    scheduling_dir + "/state_processes/state_bootup.py",           # state process id = 100, index = 0
    scheduling_dir + "/state_processes/state_detumble.py",         # state process id = 101, index = 1
    scheduling_dir + "/state_processes/state_charge.py",           # state process id = 102, index = 2
    scheduling_dir + "/state_processes/state_antennas.py",         # state process id = 103, index = 3
]

# STATE PROCESS IDS
# start at 100 to allow for process ids 0-99 to be data processes
state_processes_ids = {"bootup" : 100,
                       "detumble" : 101,
                       "charge" : 102}


# RUN A PROCESS
def run_script(script_name, output_queue, stop_event, process_id):
    # to run the script, we need an interpreter, the python interpreter is located at the file "/usr/bin/python3"
    # PIPE = make a standard pipe, which allows for standard communication across channels, in this case the I/O channel 
    process = subprocess.Popen(["/usr/bin/python3", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while not stop_event.is_set():
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_queue.put((process_id, output.strip()))


# CREATE NEW STATE PROCESS 
def startup_state_process(process_id, dynamic_vars):
    dynamic_vars["stop_event" + str(process_id)] = multiprocessing.Event()
    dynamic_vars["process" + str(process_id)]  = multiprocessing.Process(target=run_script, args=(state_processes[process_id-100], output_queue, dynamic_vars["stop_event" + str(process_id)], process_id))
    dynamic_vars["process" + str(process_id)].start()
    processes.append(dynamic_vars["process" + str(process_id)])


# FUNCTION TO STOP PROCESS
def stop_state_process(process_id, dynamic_vars):
    stop_event = dynamic_vars.get("stop_event" + str(process_id))
    process = dynamic_vars.get("process" + str(process_id))
    
    if stop_event is not None:
        stop_event.set()  # Signal the process to stop if it checks for this event
        
    if process is not None:
        process.terminate()  # Forcefully terminate the process
        process.join()  # Wait for the process to terminate

def extract_data(output):
    data_value = re.search(r'\[([-+]?\d+)\]', output)
    if data_value:
        return data_value.group(1)

# MAIN FUNCTION
if __name__ == "__main__":

    # SETUP MULTIPROCESSING
    output_queue = multiprocessing.Queue()
    processes = []

    # FIRE THE "BOOTUP STATE PROCESS"
    stop_event100 = multiprocessing.Event()
    process100 = multiprocessing.Process(target=run_script, args=(state_processes[0], output_queue, stop_event100, 100))
    process100.start()
    processes.append(process100)


    # FIRE UP "DATA PROCESSES"
    dynamic_vars = {}
    for i in range(1, len(data_processes) + 1):
        dynamic_vars["stop_event" + str(i)] = multiprocessing.Event()
        dynamic_vars["process" + str(i)]  = multiprocessing.Process(target=run_script, args=(data_processes[i-1], output_queue, dynamic_vars["stop_event" + str(i)], i))
        dynamic_vars["process" + str(i)].start()
        processes.append(dynamic_vars["process" + str(i)])
    
    current_state = "bootup"

    while True:
        try:
            # OUTPUT PRINT STATEMENTS FROM PROCESSES
            process_id, output = output_queue.get_nowait()
            print(f"{output}")
            
            # OVERRIDE SWITCH
            # DATA_BP = battery percentage
            # regardless of the current state, these MUST be done
            if "DATA_BP" in output and int(output[11:-1].strip()) <= 20:
                current_state = "charge"
                startup_state_process(process_id + 1, dynamic_vars)
                continue


            # STARTUP => ...
            if "[STATE_BOOTUP] [Ended]" in output:
                # start up DETUMBLE
                current_state = "detumble"
                startup_state_process(101, dynamic_vars)


            # DETUMBLE => ...
            if current_state == "detumble":
                # if this line has data, extract it
                value = extract_data(output)
                # see if this threshold occurs: this will always have data
                if "DATA_IMU_AV" in output and int(value) <= 0: # TODO: fine-tune the threshold on lower and upper
                    current_state = "charge"
                    # stop DETUMBLE
                    stop_state_process(101, dynamic_vars)
                    print("\n[STATE_DETUMBLE] [Ended] \n", flush = True)
                    # start up CHARGE
                    startup_state_process(102, dynamic_vars)
                    continue


            # CHARGE => ...
            if current_state == "charge":
                # if this line has data, extract it
                value = extract_data(output)
                if "DATA_BATTERY_BP" in output and int(value) >= 95:
                    current_state = "antennas"
                    # stop CHARGE
                    stop_state_process(102, dynamic_vars)
                    print("\n[STATE_CHARGE] [Ended] \n", flush = True)
                    # start up ANTENNAS
                    startup_state_process(103, dynamic_vars)
                    continue


            # ANTENNAS => ...
            if current_state == "atennas":
                if "DATA_BP" in output and int(output[11:-1].strip()) > 50:
                    if "DATA_EA" in output: # IF WE ARE OVER EARTH
                        current_state = "comms"
                        # startup_state_process(process_id + 1, dynamic_vars)
                        continue


            # COMMS => ...
            if current_state == "comms":
                if "DATA_BP" in output and int(output[11:-1].strip()) > 50:
                    if "DATA_AV" in output and int(output[11:-1].strip()) <= 0: # maybe fine-tune the threshold on lower and upper
                        current_state = "deploy_payload"
                        # startup_state_process(process_id + 1, dynamic_vars)
                        continue
           

            # DEPLOY PAYLOAD => ...
            if current_state == "deploy_payload":
                if "DATA_BP" in output and int(output[11:-1].strip()) > 30:
                    current_state = "orient_payload"
                    # startup_state_process(process_id + 1, dynamic_vars)
                    continue
            

            # ORIENT PAYLOAD => ...
            if current_state == "orient_payload":
                if "DATA_EA" in output: # IF WE ARE OVER EARTH
                    current_state = "comms"
                    # startup_state_process(process_id + 1, dynamic_vars)
                elif "DATA_BP" in output and int(output[11:-1].strip()) > 30: 
                    current_state = "comms"
                    # startup_state_process(process_id + 1, dynamic_vars)
                    continue


            # DECIDE TO KILL
            # if process_id == 1:
            #   if "4" in output or "5" in output:
            #        print("Process 1 terminated, due to data output")
            #        processes[process_id].terminate()

        except queue.Empty:
            pass
    
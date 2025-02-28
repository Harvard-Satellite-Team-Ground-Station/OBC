# scheduler.py



# ++++++++++++++ Imports/Installs ++++++++++++++ #
import multiprocessing
import subprocess
import queue
import os
import re
import config



# ++++++++++++++ Global Variables ++++++++++++++ #
# checkpoints for FSM
checkpoint = False
deployed_already = False

# processes
    # Each file will run in its own process
    # Data processes run forever
    # Data processes are assigned IDs 0-99
    # State processes start/end dynamically
    # State processes are assigned IDs 100+
scheduling_dir = os.path.dirname(os.path.abspath(__file__))

# Useful to print out which processes are active at a given time
active_process_dict = {}
active_process_list = []

data_files = [ # insert relative paths to these files
    scheduling_dir + "/data_processes/data_battery.py",            # data process id = 1
    scheduling_dir + "/data_processes/data_imu.py",                # data process id = 2
    scheduling_dir + "/data_processes/data_star_tracker.py",       # data process id = 3
]

state_files = [ # insert relative paths to these files
    scheduling_dir + "/state_processes/state_bootup.py",           # state process id = 100, index = 0
    scheduling_dir + "/state_processes/state_detumble.py",         # state process id = 101, index = 1
    scheduling_dir + "/state_processes/state_charge.py",           # state process id = 102, index = 2
    scheduling_dir + "/state_processes/state_antennas.py",         # state process id = 103, index = 3
    scheduling_dir + "/state_processes/state_comms.py",            # state process id = 104, index = 4
    scheduling_dir + "/state_processes/state_deploy.py",           # state process id = 105, index = 5
    scheduling_dir + "/state_processes/state_orient.py",           # state process id = 106, index = 6
]

state_processes_ids = {"bootup"     : 100,
                       "detumble"   : 101,
                       "charge"     : 102,
                       "antennas"   : 103,
                       "comms"      : 104,
                       "deploy"     : 105,
                       "orient"     : 106}


# +++++++++++++++++ Functions: Setup +++++++++++++++++ #

def start_process(process_id, process_dict, process_files=state_files, process_list=[]):
    """ 
    Start a process.
    process_id        the state process ID we assign, a number 100+
    process_dict      dictionary that holds two kinds of values: 
                      process#: multiprocessing object for a process 
                      stop_event#: multiprocessing method to stop a process object
    process_list      a list-format of the process_dict, for printing to terminal
    process_files     these are the code files the processes in the dict will run
                      are we using the 'data_processes' list of files or 'state_processes' list of files
    """
    index = 1
    if process_id >= 100:
        index = 100
    process_dict["stop_event" + str(process_id)] = multiprocessing.Event()
    process_dict["process" + str(process_id)]  = multiprocessing.Process(target=run_script, args=(process_files[process_id-index], output_queue, process_dict["stop_event" + str(process_id)], process_id))
    process_dict["process" + str(process_id)].start()
    process_list.append(process_id)
    print("\033[38;5;12m Active Processes:", process_list, "\033[0m")

def stop_process(process_id, process_dict, process_list=[]):
    """ 
    Stop a state process. 
    """
    stop_event_key = f"stop_event{process_id}"
    stop_event = process_dict.get(stop_event_key)
    process_key = f"process{process_id}"
    process = process_dict.get(process_key)
    
    if stop_event is not None:
        stop_event.set()    # Signal process to stop if it checks for this event
        
    if process is not None:
        process.terminate() # Forcefully terminate the process
        process.join()      # Ensure the process is fully terminated
        del process_dict[stop_event_key]  
        del process_dict[process_key]
        process_list.remove(process_id)

def run_script(script_name, output_queue, stop_event, process_id):
    """ 
    Stop a state process. 
    to run the script, we need an interpreter, the python interpreter is located at the file "/usr/bin/python3"
    PIPE = make a standard pipe, which allows for standard communication across channels, in this case the I/O channel 
    """
    process = subprocess.Popen([config.PYTHON_FILE_COMPILER, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while not stop_event.is_set():
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_queue.put((process_id, output.strip()))

def extract_data(output):
    data_value = re.search(r'\[([-+]?\d+)\]', output)
    if data_value:
        return data_value.group(1)
    
def extract_data_multiple(output):
    data_values = re.findall(r'\[([-+]?\d+(?:,\s*[-+]?\d+)*)\]', output)
    values_list = [int(num) for num in data_values[0].split(',')]
    return values_list


# +++++++++++++++++ Functions: Main +++++++++++++++++ #
if __name__ == "__main__":

    # Setup multiprocessing
    output_queue = multiprocessing.Queue()
    processes = []

    # Fire Up Bootup State Process
    active_process_dict["stop_event100"] = multiprocessing.Event()
    active_process_dict["process100"]  = multiprocessing.Process(target=run_script, args=(state_files[0], output_queue, active_process_dict["stop_event100"], 100))
    active_process_dict["process100"].start()
    active_process_list.append(100)

    # Fire Up Data Processes
    for i in range(1, len(data_files) + 1):
        start_process(i, active_process_dict, process_files=data_files, process_list=active_process_list)

    current_state = "bootup"
    while True:
        try:
            # Output print statements from processes
            process_id, output = output_queue.get_nowait()
            print(f"{output}")
            
            # Override switch
            # DATA_BP = battery percentage
            # regardless of the current state, these MUST be done
            if "DATA_BP" in output and int(output[11:-1].strip()) <= 20:
                current_state = "charge"
                start_process(process_id + 1, active_process_dict, process_files=state_files, process_list=active_process_list)
                continue

            # Startup => ...
            if "[STATE_BOOTUP] [Ended]" in output:
                # start up DETUMBLE
                current_state = "detumble"
                start_process(101, active_process_dict, process_files=state_files, process_list=active_process_list)

            # Detumble => ...
            if current_state == "detumble":
                # if this line has data, extract it
                value = extract_data(output)
                # see if this threshold occurs: this will always have data
                if "DATA_IMU_AV" in output and int(value) <= 0: # TODO: fine-tune the threshold on lower and upper
                    current_state = "charge"
                    # stop DETUMBLE
                    stop_process(101, active_process_dict, active_process_list)
                    print("\n \033[38;5;196m[STATE_DETUMBLE] [Ended]\033[0m \n", flush=True)
                    # start up CHARGE
                    start_process(102, active_process_dict, process_files=state_files, process_list=active_process_list)
                    continue

            # Charge => ...
            if current_state == "charge":
                # if this line has data, extract it
                value = extract_data(output)
                # TODO: change to 95, currently at 75 to allow for faster testing
                if "DATA_BATTERY_BP" in output and int(value) >= 75:
                    current_state = "antennas"
                    # stop CHARGE
                    stop_process(102, active_process_dict, active_process_list)
                    print("\n \033[38;5;196m[STATE_CHARGE] [Ended]\033[0m \n", flush=True)
                    # start up ANTENNAS
                    start_process(103, active_process_dict, process_files=state_files, process_list=active_process_list)
                    continue

            # Antennas => ...
            if current_state == "antennas":
                # if this line has data, extract it
                value = extract_data(output)
                if "DATA_BATTERY_BP" in output and int(value) >= 50:
                    checkpoint = True
                if checkpoint and "DATA_STARTRACKER_POS" in output:
                    values = extract_data_multiple(output)
                    if values[0] > 90 and values[1] > 90 and values[2] > 90:
                        checkpoint = False
                        current_state = "comms"
                        # stop ANTENNAS
                        stop_process(103, active_process_dict, active_process_list)
                        print("\n \033[38;5;196m[STATE_ANTENNAS] [Ended]\033[0m \n", flush=True)
                        # start up COMMS
                        start_process(104, active_process_dict, process_files=state_files, process_list=active_process_list)
                        continue

            # Comms => ...
            if current_state == "comms":
                # if this line has data, extract it
                value = extract_data(output)
                if "DATA_BATTERY_BP" in output and int(value) >= 50:
                    checkpoint = True
                # TODO: change threshold
                if checkpoint and "DATA_IMU_AV" in output and int(value) <= 1:
                    checkpoint = False
                    # stop COMMS
                    stop_process(104, active_process_dict, active_process_list)
                    print("\n \033[38;5;196m[STATE_COMMS] [Ended]\033[0m \n", flush=True)
                    if not deployed_already:
                        # start up DEPLOY
                        deployed_already = True
                        current_state = "deploy"
                        start_process(105, active_process_dict, process_files=state_files, process_list=active_process_list)
                        continue
                    else:
                        # start up ORIENT
                        current_state = "orient"
                        start_process(106, active_process_dict, process_files=state_files, process_list=active_process_list)
                        continue

            # Deploy Payload => ...
            if current_state == "deploy":
                # if this line has data, extract it
                value = extract_data(output)
                if "DATA_BATTERY_BP" in output and int(value) >= 30:
                # TODO: wait until deploy is done
                    # stop DEPLOY
                    current_state = "orient"
                    stop_process(105, active_process_dict, active_process_list)
                    print("\n \033[38;5;196m[STATE_DEPLOY] [Ended]\033[0m \n", flush=True)
                    # start up ORIENT
                    start_process(106, active_process_dict, process_files=state_files, process_list=active_process_list)
                    continue

            # Orient Payload => ...
            if current_state == "orient":
                if "DATA_STARTRACKER_POS" in output:
                    values = extract_data_multiple(output)
                    if values[0] > 90 and values[1] > 90 and values[2] > 90:
                        # TODO: wait until orient is done
                        # stop ORIENT
                        stop_process(106, active_process_dict, active_process_list)
                        print("\n \033[38;5;196m[STATE_ORIENT] [Ended]\033[0m \n", flush=True)
                        # start up COMMS
                        current_state = "comms"
                        start_process(104, active_process_dict, process_files=state_files, process_list=active_process_list)
                        continue

        except queue.Empty:
            pass
    
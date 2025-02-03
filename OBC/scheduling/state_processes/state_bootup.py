# ///////////////////////////////////////////////////////////////// #
# BOOTUP STATE
# ///////////////////////////////////////////////////////////////// #


# IMPORTS
import time


# FUNCTIONS
def __init__():
    on_loop()


def on_loop():
    # TO-DO: do some setup functions
    # ....
    time.sleep(1) 


# MAIN FUNCTION
print("\n \033[38;5;46m[STATE_BOOTUP] [Started]\033[0m \n", flush=True)
__init__()
print("\n \033[38;5;196m[STATE_BOOTUP] [Ended]\033[0m \n", flush=True)


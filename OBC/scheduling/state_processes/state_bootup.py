# ///////////////////////////////////////////////////////////////// #
# BOOTUP STATE
# ///////////////////////////////////////////////////////////////// #
import time


# FUNCTIONS
def __init__():
    print("Bootup State Begin")
    on_loop(5)


def on_loop():
    # TO-DO: do some setup functions
    # ....
    time.sleep(5) 


# MAIN FUNCTION
__init__()
print("Bootup State Complete", flush = True)


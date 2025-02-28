# subs_magnetorquer.py



# ++++++++++++++ Imports/Installs ++++++++++++++ #
from subsystems import config



# ++++++++++++++ Class Definition ++++++++++++++ # 
class SubsystemMagnetorquer:
    def __init__(self):
        self.port_input = config.PORT_MAGNETORQUER_INPUT
        self.port_output = config.PORT_MAGNETORQUER_OUTPUT
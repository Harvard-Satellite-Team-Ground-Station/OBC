# subs_antenna.py



# ++++++++++++++ Imports/Installs ++++++++++++++ #
from subsystems import config



# ++++++++++++++ Class Definition ++++++++++++++ # 
class SubsystemAntenna:
    def __init__(self):
        self.port_input = config.PORT_ANTENNA_INPUT
        self.port_output = config.PORT_ANTENNA_OUTPUT
# subs_nithinol.py



# ++++++++++++++ Imports/Installs ++++++++++++++ #
from subsystems import config



# ++++++++++++++ Class Definition ++++++++++++++ # 
class SubsystemNithinol:
    def __init__(self):
        self.port_input = config.PORT_NITHINOL_INPUT
        self.port_output = config.PORT_NITHINOL_OUTPUT
# subs_camera.py



# ++++++++++++++ Imports/Installs ++++++++++++++ #
from subsystems import config



# ++++++++++++++ Class Definition ++++++++++++++ # 
class SubsystemCamera:
    def __init__(self):
        self.port_input = config.PORT_CAMERA_INPUT
        self.port_output = config.PORT_CAMERA_OUTPUT
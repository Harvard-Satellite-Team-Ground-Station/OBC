# subs_battery.py



# ++++++++++++++ Imports/Installs ++++++++++++++ #
import can
from subsystems import config


# ++++++++++++++ Class Definition ++++++++++++++ # 
class SubsystemBattery:
    def __init__(self):
        self.bus = can.interface.Bus(channel=config.PORT_BATTERY_INPUT, bustype='socketcan')

    def data_func_battery_percentage(self):
        """
        Read in voltage from pin, 
        Conversion-chart for voltage to battery percentage
        """
        # Read ADC value (0-1.8V)
        try:
            msg = self.bus.recv(timeout=1.0)
            if msg and msg.arbitration_id == config.CAN_ID_BATTERY_STATUS:
                value = msg.data[0]  
                # Since battery is (0-4.2V), scale by 2.34
                voltage = value * 2.34
                # Reverse voltage divider scaling (assuming 22kΩ / 47kΩ divider)
                voltage = voltage * (69 / 22) 
                if voltage >= 4.2:
                    return 100
                elif voltage >= 3.95:
                    return 75
                elif voltage >= 3.7:
                    return 50
                elif voltage >= 3.5:
                    return 25
                elif voltage >= 3.2:
                    return 0
                else:
                    return -1
            return -1
        except can.CanError as e:
            print(f"[Battery] CAN error: {e}")
            return -1
    
        


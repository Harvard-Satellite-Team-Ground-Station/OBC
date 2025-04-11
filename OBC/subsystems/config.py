# config.py



# ++++++++++++++ Imports/Installs ++++++++++++++ #



# ++++++++++++++ Can-Bus Variables ++++++++++++++ #
"""
Each can-bus is a collection of insertion pins where you can put wires
Each can-bus will therefore be able to handle multiple sub-systems
CAN_BUS_[subsystem]
"""
CAN_BUS_IMU                     = 'can1'
CAN_BUS_MAGNETORQUER            = 'can1'
CAN_BUS_NITHINOL                = 'can2'
CAN_BUS_CAMERA                  = 'can2'
CAN_BUS_BATTERY                 = ''        # it has its own input can bus
CAN_BUS_ANTENNA                 = ''        # it has its own input can bus

""" 
PORT_IMU_INPUT                  = #GPIO.setup("P8_7", GPIO.IN)
PORT_IMU_OUTPUT                 = #GPIO.setup("P8_8", GPIO.OUT)
PORT_MAGNETORQUER_INPUT         = #GPIO.setup("P8_11", GPIO.IN)
PORT_MAGNETORQUER_OUTPUT        = #GPIO.setup("P8_12", GPIO.OUT)
PORT_BATTERY_INPUT              = #GPIO.setup("P8_16", GPIO.IN)
PORT_NITHINOL_INPUT             = #GPIO.setup("P8_17", GPIO.IN)
PORT_NITHINOL_OUTPUT            = #GPIO.setup("P8_18", GPIO.OUT)
PORT_CAMERA_INPUT               = #GPIO.setup("P9_23", GPIO.IN)
PORT_CAMERA_OUTPUT              = #GPIO.setup("P9_24", GPIO.OUT)
PORT_ANTENNA_INPUT              = #GPIO.setup("P9_25", GPIO.IN)
PORT_ANTENNA_OUTPUT             = #GPIO.setup("P9_26", GPIO.OUT)
"""


# ++++++++++++++ Can-ID Variables ++++++++++++++ #
"""
To know which wires should correspond to what, we'll use can-ids
These correspond to the literal pin inputs
CAN_ID_[subsystem]_[input/output]_[description]
"""
CAN_ID_BATTERY_INPUT_STATUS           = 0x100       # on can_bus 0, for pin 0x100, this'll be the wire for getting status
CAN_ID_BATTERY_INPUT_TEMP             = 0x101       # on can_bus 0, for pin 0x101, this'll be the wire for getting temp


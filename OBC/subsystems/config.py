# config.py



# ++++++++++++++ Imports/Installs ++++++++++++++ #
import Adafruit_BBIO.GPIO as GPIO



# ++++++++++++++ Global Variables ++++++++++++++ #
PORT_IMU_INPUT                  = GPIO.setup("P8_7", GPIO.IN)
PORT_IMU_OUTPUT                 = GPIO.setup("P8_8", GPIO.OUT)
PORT_MAGNETORQUER_INPUT         = GPIO.setup("P8_11", GPIO.IN)
PORT_MAGNETORQUER_OUTPUT        = GPIO.setup("P8_12", GPIO.OUT)
PORT_BATTERY_INPUT              = GPIO.setup("P8_16", GPIO.IN)
PORT_NITHINOL_INPUT             = GPIO.setup("P8_17", GPIO.IN)
PORT_NITHINOL_OUTPUT            = GPIO.setup("P8_18", GPIO.OUT)
PORT_CAMERA_INPUT               = GPIO.setup("P9_23", GPIO.IN)
PORT_CAMERA_OUTPUT              = GPIO.setup("P9_24", GPIO.OUT)
PORT_ANTENNA_INPUT              = GPIO.setup("P9_25", GPIO.IN)
PORT_ANTENNA_OUTPUT             = GPIO.setup("P9_26", GPIO.OUT)


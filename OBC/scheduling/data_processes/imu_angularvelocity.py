import time
import random
from ...subsystems.imu import IMU

# in time, we won't generate a random int, it'll be a function from the subsystem that we call

gyro = IMU()

while True:
    time.sleep(0.5) # Interval to run measurements on

    acc_x, acc_y, acc_z, vel_x, vel_y, vel_z = gyro.get_velocity()

    output = "[DATA_VX] [" + str(vel_x) + "]" + "[DATA_VY] [" + str(vel_y) + "]" + "[DATA_VZ] [" + str(vel_z) + "]"
    
    print(output, flush=True)


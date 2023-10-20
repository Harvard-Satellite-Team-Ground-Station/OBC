import board
import busio
import adafruit_bno055
import time

class IMU:
    def __init__(self, i2c):
        # i2c = busio.I2C(board.SCL, board.SDA) # TODO how to load this in
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)

        self.last_val = 0xFFFF

    def temperature(self):
        result = self.sensor.temperature
        if abs(result - last_val) == 128:
            result = self.sensor.temperature
            if abs(result - last_val) == 128:
                return 0b00111111 & result
        last_val = result
        return result

    def get_accleration(self):
        return self.sensor.acceleration

    def get_magnetic(self):
        return self.sensor.magnetic

    def get_gyro(self):
        return self.sensor.gyro

    def get_euler_angle(self):
        return self.sensor.euler

    def get_quaternion(self):
            return self.sensor.quaternion
    
    def get_linear_acceleration(self):
        return self.sensor.linear_acceleration
    
    def get_gravity(self):
        return self.sensor.gravity
    
    # def get_velocity(self): TODO: linear velocity and angular velocity
        # calculations

    # def get_position(self):

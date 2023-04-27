#not used anymore,kept in repository for any potential future reference reasons
import board
import busio
import adafruit_bno055
import time
import math

i2c = busio.I2C(board.GP1, board.GP0)  # uses board.SCL and board.SDA
head_bno = adafruit_bno055.BNO055_I2C(i2c, address=0x28)
chest_bno = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

def acceleration(sensor):
    global last_val  # pylint: disable=global-statement
    result = sensor.acceleration
    result = list(result)
    result = [math.ceil(x*100)/100 for x in result ]
    return result

def gyro(sensor):
    global last_val  # pylint: disable=global-statement
    result = sensor.gyro
    result = list(result)
    result = [math.ceil(x*100)/100 for x in result ]
    return result

def euler(sensor):
    global last_val  # pylint: disable=global-statement
    result = sensor.euler
    result = list(result)
    result = [math.ceil(x*100)/100 for x in result ]
    return result


while True:
    head_accel = acceleration(head_bno)
    chest_accel = acceleration(chest_bno)
    head_gyro = gyro(head_bno)
    chest_gyro = gyro(chest_bno)
    head_euler = euler(head_bno)
    chest_euler = euler(chest_bno)
    print("Chest Acceleration: " + str(chest_accel))
    print("Chest gyro: " + str(chest_gyro))
    print("Chest Euler: " + str(chest_euler))
    
    time.sleep(1)

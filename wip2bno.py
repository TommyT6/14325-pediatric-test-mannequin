import os
# import ipaddress
import wifi
import socketpool
import time
import microcontroller
import board
import busio
import adafruit_bno055
import math

# Device ID
ID_head = (0,)
ID_chest = (1,)
IDArray = [ID_head, ID_chest]

#Change classifier here depending on code
c_accel = (0,)
c_angVel = (1,)
c_euler = (2,)

#change this to 1 to reset the microcontroller in case of failure
controller_reset = 0

i2c = busio.I2C(board.GP1, board.GP0)  # uses board.SCL and board.SDA
head_bno = adafruit_bno055.BNO055_I2C(i2c, address=0x28)
chest_bno = adafruit_bno055.BNO055_I2C(i2c, address=0x29)
sensorArray = [head_bno, chest_bno]

address = "172.16.150.148"
port = 5000
CompIP = (address,port)
#myPort =
myIP = str(wifi.radio.ipv4_address)
        
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

print("Connecting to WiFi...")

try:
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
except Exception as e:
    print(e)
    print("There was a problem connnecting to WiFi")
    time.sleep(1)
else:
    print("Connected to WiFi")

# Create socket for Pico
pool = socketpool.SocketPool(wifi.radio)
mySock = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

# Connect to laptop
print("Connecting to the laptop")
while True:
    try:
        mySock.connect(CompIP)
    except Exception as e:
        print(e)
        print("There was a problem connecting to the laptop, restarting microcontroller in 3 seconds")
        time.sleep(1)
        if controller_reset == 1:
            microcontroller.reset()
        continue
    else:
        print("Connected to the laptop successfully")
        break

time.sleep(1)
print("Starting to send data...")
time.sleep(0.5)

# Receive and send data from sensor repeatedly
while True:
    for x in range(2):
        # Retrieve and send acceleration
        try:
            data = (acceleration(sensorArray[x]),)
            # append classifier and device ID to data
            data = IDArray[x] + c_accel + data
            data = str(data)
        except:
            print("Error collecting data from sensor")    
        try:
            mySock.send(data)
            print("Sending: " + data + "\n")
        except Exception as e: 
            print(e)
        time.sleep(0.005)

        # Retrieve and send angular velocity
        try:
            data = (gyro(sensorArray[x]),)
            # append classifier and device ID to data
            data = IDArray[x] + c_angVel + data
            data = str(data)
        except:
            print("Error collecting data from sensor")    
        try:
            mySock.send(data)
            print("Sending: " + data + "\n")
        except Exception as e: 
            print(e)
        time.sleep(0.005)
    
        # Retrieve and send euler angle
        try:
            data = (euler(sensorArray[x]),)
            # append classifier and device ID to data
            data = IDArray[x] + c_euler + data
            data = str(data)
        except:
            print("Error collecting data from sensor")    
        try:
            mySock.send(data)
            print("Sending: " + data + "\n")
        except Exception as e: 
            print(e)
        time.sleep(0.005)



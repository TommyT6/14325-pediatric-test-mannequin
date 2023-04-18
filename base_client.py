import os
import ipaddress
import wifi
import socketpool
import time
import microcontroller
import board
import busio
import adafruit_bno055
import math

#change this to 1 to reset the microcontroller in case of failure
controller_reset = 0

i2c = busio.I2C(board.GP1, board.GP0)  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)
last_val = 0xFFFF

address = "172.16.150.144"
port = 50000
CompIP = (address,port)
myPort = 5000
myIP = str(wifi.radio.ipv4_address)
        
def acceleration():
    global last_val  # pylint: disable=global-statement
    result = sensor.acceleration
    result = list(result)
    result = [math.ceil(x*100)/100 for x in result ]
    return result

#Change classifier here depending on code
classifier = (0,)

print("Connecting to WiFi")

try:
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
except Exception as e:
    print(e)
    print("There was a problem connnecting to WiFi")
    time.sleep(1)
else:
    print("Connected to WiFi")

#Create socket for Pico
pool = socketpool.SocketPool(wifi.radio)
mySock = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

#Connect to laptop
print("Connecting to the laptop")
while True:
    try:
        mySock.connect(CompIP)
    except Exception as e:
        print(e)
        print("There was a problem connecting to the laptop, restarting microcontroller in 3 seconds")
        time.sleep(3)
        if controller_reset == 1:
            microcontroller.reset()
        continue
    else:
        print("Connected to the laptop successfully")
        break

time.sleep(1)
print("Starting to send data")
time.sleep(0.5)
#receive and send data from sensor
while True:
    try:
        #receive data from sensor
        data = (acceleration(),)
        #append classifier to data
        data = classifier + data
        data = str(data)
    except:
        print("Problem collecting data from sensor")    
    try:
        #Send the data
        mySock.send(data)
        print("Sending: " + data + "\n")
    except Exception as e: print(e)
    time.sleep(1)
    




        
    
    







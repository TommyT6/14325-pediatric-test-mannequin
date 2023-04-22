# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import re

def printAccel(data):
    
    accelX = float(data[1])
    accelY = float(data[2])
    accelZ = float(data[3])
    
    print("Acceleration: x = " + str(accelX) + " m/s^2, y = " + str(accelY) + " m/s^2, z = " + str(accelZ) + " m/s^2")

def printEuler(data):
    
    eulerX = float(data[1])
    eulerY = float(data[2])
    eulerZ = float(data[3])
    
    print("Euler Angle: x = " + str(eulerX) + ", y = " + str(eulerY) + ", z = " + str(eulerZ))

classifier_accel = (0,)
classifier_euler = (1,)

data_accel = (0.521435, 0.012345, 8.863465,)
data_euler = (0.362634, 0.269732, 0.517492,)

print("Printing tuples... This is the data extracted from the sensors.")
print("data_accel: " + str(data_accel))
print("data_euler: " + str(data_euler))
print("")

packet_accel = str(classifier_accel + data_accel)
packet_euler = str(classifier_euler + data_euler)

print("Printing packets... This is the data sent through Wi-Fi.")
print("packet_accel: " + packet_accel)
print("packet_euler: " + packet_euler)
print("")

regex_accel = re.findall(r"[-+]?(?:\d*\.*\d+)", packet_accel)
regex_euler = re.findall(r"[-+]?(?:\d*\.*\d+)", packet_euler)

print("Printing regex output... This is the parsed data.")
print("regex_accel: " + str(regex_accel))
print("regex_euler: " + str(regex_euler))
print("")

print("Printing final data... This contains the actual float values to be inserted.")
if(int(regex_accel[0]) == 0):
    printAccel(regex_accel)

if(int(regex_euler[0]) == 1):
    printEuler(regex_euler)
    
    
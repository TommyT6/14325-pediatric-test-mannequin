from machine import Pin
from src.hx711 import *
import time

# 1. initialize the hx711 with pin 14 as clock pin, pin 15 as data pin
hx = hx711(Pin(14), Pin(15))

# 2. power up
hx.set_power(hx711.power.pwr_up)

# 3. [OPTIONAL] set gain and save it to the hx711 chip by powering down then back up
hx.set_gain(hx711.gain.gain_128)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)

# 4. wait for readings to settle
hx711.wait_settle(hx711.rate.rate_10)

# 5. read values

# hard code the calibration factor for your specific load cell and setup
cal_factor = 50000

# wait (block) until a value is read
while True:
    # get the raw value from the hx711
    raw_val = hx.get_value()
    if raw_val is not None:
        # calculate the force based on the calibration factor
        force = (raw_val / cal_factor) - 0.8  # subtracting 0.8 to remove the tare weight

        # print the force
        print("Force: %.2f" % force)
    else:
        print("Failed to get reading. Try checking your wiring.")

    time.sleep(0.1)


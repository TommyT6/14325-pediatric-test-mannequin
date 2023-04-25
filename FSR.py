from multiplex import Mux
import math
import analogio
import time

m = Mux()
resistance = 10000
def get_voltage(raw):
    return (raw * 3.3) / 65536

while True:
    for i in range(0,4):
        m.change_sig(i)
        raw = m.SIG.value
        volts = get_voltage(raw)
        fsr_resistance = resistance / (3.3 / (volts - 1 + 0.000001))
        force = fsr_resistance / 1000  # Convert to kilogram-force
        print("FSR", i + 1, "force:", force, "kgf")
        time.sleep(1)
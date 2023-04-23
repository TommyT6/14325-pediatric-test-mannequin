import time
import board
from digitalio import DigitalInOut, Direction, Pull

#Setting the pins as digital GPIO pins
s = []
s.append(DigitalInOut(board.GP5))
s.append(DigitalInOut(board.GP4))
s.append(DigitalInOut(board.GP3))
s.append(DigitalInOut(board.GP2))
SIG = DigitalInOut(board.GP1)
EN  = DigitalInOut(board.GP6)


#Set the directions of the pins
SIG.direction = Direction.INPUT
EN.direction = Direction.OUTPUT
for i in range(0,4):
    s[i].direction = Direction.INPUT

#change the input of the mux
def change_sig(num):
    bin_num = format(num,'04b')
    reverse_bin_num = bin_num[::-1]

    for i, bit in enumerate(reverse_bin_num):
        if bit == '1':
            s[3-i].pull = Pull.UP

def enable_high():
    EN.pull = Pull.UP

def enable_low():
    EN.pull = Pull.DOWN 
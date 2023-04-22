import time
import board
from digitalio import DigitalInOut, Direction, Pull

SIG = DigitalInOut(board.GP1)
S3 = DigitalInOut(board.GP2)
S2 = DigitalInOut(board.GP3)
S1 = DigitalInOut(board.GP4)
S0 = DigitalInOut(board.GP5)
EN  = DigitalInOut(board.GP6)

SIG.direction = Direction.INPUT
S3.direction = Direction.OUTPUT
S2.direction = Direction.OUTPUT
S1.direction = Direction.OUTPUT
S0.direction = Direction.OUTPUT
EN.direction = Direction.OUTPUT

def change_sig(input_num):
    if input_num == 0:
        S3.pull = Pull.DOWN
        S2.pull = Pull.DOWN
        S1.pull = Pull.DOWN
        S0.pull = Pull.DOWN
    if input_num == 1:
        S3.pull = Pull.DOWN
        S2.pull = Pull.DOWN
        S1.pull = Pull.DOWN
        S0.pull = Pull.UP
    if input_num == 2:
        S3.pull = Pull.DOWN
        S2.pull = Pull.DOWN
        S1.pull = Pull.UP
        S0.pull = Pull.DOWN
    if input_num == 3:
        S3.pull = Pull.DOWN
        S3.pull = Pull.DOWN
        S3.pull = Pull.UP
        S3.pull = Pull.UP

def enable_high():
    EN.pull = Pull.UP

def enable_low():
    EN.pull = Pull.DOWN 
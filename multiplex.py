import board
from digitalio import DigitalInOut, Direction, Pull
import analogio
#Setting the pins as digital GPIO pins

class Mux:
    def __init__(self):
        self.s = []
        self.s.append(DigitalInOut(board.GP5))
        self.s.append(DigitalInOut(board.GP4))
        self.s.append(DigitalInOut(board.GP3))
        self.s.append(DigitalInOut(board.GP2))
        self.SIG = analogio.AnalogIn(board.A0)
        self.EN  = DigitalInOut(board.GP6)

        #Set the directions of the pins
        self.EN.direction = Direction.OUTPUT
        for i in range(0,4):
            self.s[i].direction = Direction.INPUT

    #change the input of the mux
    def change_sig(self,num):
        bin_num = bin(num)[2:]  # Convert to binary and remove the '0b' prefix
        bin_num = '0' * (4 - len(bin_num)) + bin_num  # Add leading zeros
        
        for i, bit in enumerate(reversed(bin_num)):
            if bit == '1':
                self.s[3-i].pull = Pull.UP


    def enable_high(self):
        self.EN.pull = Pull.UP

    def enable_low(self):
        self.EN.pull = Pull.DOWN 

    def setSig(self,board):
        self.SIG = DigitalInOut(board)
        self.SIG.direction = Direction.INPUT

    def setEN(self,board):
        self.EN = DigitalInOut(board)
        self.EN.direction = Direction.OUTPUT

    def setSelPin(self,select,board):
        try:
            self.SIG = analogio.AnalogIn(board.A0)
            self.s[select].direction = Direction.INPUT
        except:
            print("The select must be an integer 0-3")



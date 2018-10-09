import sys
import time
from .utils import log

try:
    import RPi.GPIO as GPIO  # Only works on RPi
except ImportError:
    log.warning("RPi.GPIO not found! Using GPIO test module.")
    from .gpio import GPIO
    GPIO = GPIO()

class Stage:
    def __init__(self, xpins, ypins):
        self.xpins = xpins
        self.ypins = ypins
        self.xpos = 0
        self.ypos = 0

    @property    
    def coordinates(self):
        return (self.xpos, self.ypos)

    def set_home(self):
        self.xpos = 0
        self.ypos = 0
    
    def right(self, nsteps):
        self.step(self.xpins, nsteps=abs(nsteps))
    def left(self, nsteps):
        self.step(self.xpins, nsteps=(-1 * abs(nsteps)))
    def up(self, nsteps):
        self.step(self.ypins, nsteps=abs(nsteps))
    def down(self, nsteps):
        self.step(self.ypins, nsteps=(-1 * abs(nsteps)))
         
    def step_x(self, nsteps):
            self.step(self.xpins, nsteps)

    def step_y(self, nsteps):
        self.step(self.ypins, nsteps)

    def goto(self, x, y):
        xsteps = x - self.xpos
        ysteps = y - self.ypos
        self.step_x(xsteps) 
        self.step_y(ysteps) 
        
    def home(self):
        self.goto(0,0)
    
    def step(self, StepPins, nsteps, speed=1):
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        # Set all pins as output
        for pin in StepPins:
          GPIO.setup(pin,GPIO.OUT)
          GPIO.output(pin, False)

        # halfstep sequence
        halfstep_seq = [[1,0,0,1],
               [1,0,0,0],
               [1,1,0,0],
               [0,1,0,0],
               [0,1,1,0],
               [0,0,1,0],
               [0,0,1,1],
               [0,0,0,1]]

        sequence_len = len(halfstep_seq)

        if nsteps < 0:
            direction = -1
        else:
            direction = 1

        WaitTime = float(speed)/float(1000)

        StepCounter = 0
        for _ in range(abs(nsteps)):

          for pin in range(0, 4):
            xpin = StepPins[pin]
            if halfstep_seq[StepCounter][pin] != 0:
              GPIO.output(xpin, True)
            else:
              GPIO.output(xpin, False)

          StepCounter += direction

          # If we reach the end of the sequence
          # start again
          if (StepCounter >= sequence_len):
            StepCounter = 0
          if (StepCounter < 0):
            StepCounter = sequence_len + direction

          # Wait before moving on
          time.sleep(WaitTime)
        
        if StepPins == self.xpins:
            self.xpos += nsteps
        else:
            self.ypos += nsteps
        GPIO.cleanup()

import sys
import time
from .utils import log

try:
    # only works on RPi
    import RPi.GPIO as GPIO
except ImportError:
    # import fake GPIO module
    log.warning()
    from .gpio import GPIO

class Stage:
    def __init__(self, xpins, ypins):
        self.xpins = xpins
        self.ypins = ypins
        self.xpos = 0
        self.ypos = 0

    #TODO change to step to neg/pos int for direction
    def right(self, nsteps):
        self.step(self.xpins, direction=-1, nsteps=nsteps)
    def left(self, nsteps):
        self.step(self.xpins, direction=1, nsteps=nsteps)
    def up(self, nsteps):
        self.step(self.ypins, direction=1, nsteps=nsteps)
    def down(self, nsteps):
        self.step(self.ypins, direction=-1, nsteps=nsteps)
        
    def set_home(self):
        self.xpos = 0
        self.ypos = 0
    
    @property    
    def coordinates(self):
        return (self.xpos, self.ypos)
        
    def goto(self, x, y):
        xsteps = x - self.xpos
        # self.step(xsteps) 
        if xsteps < 0:
            self.right(abs(xsteps))
        elif xsteps > 0:
            self.left(xsteps)
        
        ysteps = y - self.ypos
        if ysteps < 0:
            self.down(abs(ysteps))
        elif ysteps > 0:
            self.up(ysteps)
        
    def home(self):
        # x
        # self.goto(0,0)
        if self.xpos < 0:
            self.left(abs(self.xpos))
        elif self.xpos > 0:
            self.right(self.xpos)
        # y
        if self.ypos < 0:
            self.up(abs(self.ypos))
        elif self.ypos > 0:
            self.down(self.ypos)
        
    def step(self, pins, direction=1, nsteps=1000, speed=1):
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        StepPins = pins
        # Set all pins as output
        for pin in StepPins:
          GPIO.setup(pin,GPIO.OUT)
          GPIO.output(pin, False)

        # Define advanced sequence
        # as shown in manufacturers datasheet
        Seq = [[1,0,0,1],
               [1,0,0,0],
               [1,1,0,0],
               [0,1,0,0],
               [0,1,1,0],
               [0,0,1,0],
               [0,0,1,1],
               [0,0,0,1]]

        StepCount = len(Seq)
        StepDir = direction # Set to 1 or 2 for clockwise
                    # Set to -1 or -2 for anti-clockwise

        # Read wait time from command line
        wait = 1

        if wait:
          WaitTime = float(wait)/float(1000)
        else:
          WaitTime = 10/float(1000)

        # Initialise variables
        StepCounter = 0

        # Start main loop
        for _ in range (nsteps):

          for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin]!=0:
              GPIO.output(xpin, True)
            else:
              GPIO.output(xpin, False)

          StepCounter += StepDir

          # If we reach the end of the sequence
          # start again
          if (StepCounter>=StepCount):
            StepCounter = 0
          if (StepCounter<0):
            StepCounter = StepCount+StepDir

          # Wait before moving on
          time.sleep(WaitTime)
        
        if pins == self.xpins:
            self.xpos += direction * nsteps
        else:
            self.ypos += direction * nsteps
        GPIO.cleanup()

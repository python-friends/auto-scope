import sys
import time
from .utils import log
from .core import step


class Focus:

    def __init__(self, pins):
        self.pins = pins
        self.postion = 0

    def set_home(self):
        self.postion = 0
    
    def up(self, nsteps):
        step(self.pins, nsteps=abs(nsteps))

    def down(self, nsteps):
        step(self.pins, nsteps=(-1 * abs(nsteps)))

    def goto(self, postion):
        nsteps = postion - self.postion
        step(self.pins, nsteps) 
        
    def home(self):
        self.goto(0)
    
    
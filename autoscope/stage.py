from .core import step

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

    def step_x(self, nsteps, speed=10):
        self.xpos += step(self.xpins, nsteps, speed=speed)

    def step_y(self, nsteps, speed=10):
        self.ypos += step(self.ypins, nsteps, speed=speed)

    def right(self, nsteps, speed=10):
        self.step_x(abs(nsteps), speed=speed)

    def left(self, nsteps, speed=10):
        self.step_x(nsteps=(-1 * abs(nsteps)), speed=speed)

    def backward(self, nsteps, speed=10):
        self.step_y(nsteps=abs(nsteps), speed=speed)
        
    def forward(self, nsteps, speed=10):
        self.step_y(nsteps=(-1 * abs(nsteps)), speed=speed)
         
    def goto(self, x, y, speed=10):
        xsteps = x - self.xpos
        ysteps = y - self.ypos
        self.step_x(xsteps, speed=speed) 
        self.step_y(ysteps, speed=speed) 
        
    def home(self, speed=2):
        self.goto(0,0, speed=speed)

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

    def step_x(self, nsteps):
        self.xpos += step(self.xpins, nsteps)

    def step_y(self, nsteps):
        self.ypos += step(self.ypins, nsteps)

    def right(self, nsteps):
        self.step_x(abs(nsteps))

    def left(self, nsteps):
        self.step_x(nsteps=(-1 * abs(nsteps)))

    def backward(self, nsteps):
        self.step_y(nsteps=abs(nsteps))
        
    def forward(self, nsteps):
        self.step_y(nsteps=(-1 * abs(nsteps)))
         
    def goto(self, x, y):
        xsteps = x - self.xpos
        ysteps = y - self.ypos
        self.step_x(xsteps) 
        self.step_y(ysteps) 
        
    def home(self):
        self.goto(0,0)

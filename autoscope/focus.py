from .core import step


class Focus:

    def __init__(self, zpins):
        self.zpins = zpins
        self.zpos = 0

    def set_home(self):
        self.zpos = 0

    def step_z(self, nsteps):
        self.zpos += step(self.zpins, nsteps)
    
    def up(self, nsteps):
        self.step_z(nsteps=abs(nsteps))

    def down(self, nsteps):
        self.step_z(nsteps=(-1 * abs(nsteps)))

    def goto(self, postion):
        nsteps = postion - self.zpos
        self.step_z(nsteps) 
        
    def home(self):
        self.goto(0)
    
    
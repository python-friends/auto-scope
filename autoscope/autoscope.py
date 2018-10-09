from .stage import Stage
from .focus import Focus

class Autoscope:

    def __init__(self, xpins, ypins, zpins):
        self.stage = Stage(xpins, ypins)
        self.focus = Focus(zpins)

    @property    
    def coordinates(self):
        return (self.stage.xpos, self.stage.ypos, self.focus.zpos)


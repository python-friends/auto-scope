from .stage import Stage
from .focus import Focus
from .camera import Camera

class Autoscope:

    def __init__(self, xpins, ypins, zpins):
        self.stage = Stage(xpins, ypins)
        self.focus = Focus(zpins)
        self.camera = Camera(self.focus)

    @property    
    def coordinates(self):
        return (self.stage.xpos, self.stage.ypos, self.focus.zpos)

    def auto_focus(self, thresh=150, course_stepsize=10, course_maxsteps=400):
        # uses the corse, fine, find algo.
        corse_x1, corse_y1 = self.camera.scan(
            maxsteps=course_maxsteps, 
            stepsize=course_stepsize,
            thresh=150,
            direction=-1)
        fine_x2, fine_y2 = self.camera.scan(
            maxsteps=2*course_stepsize, 
            stepsize=1,
            thresh= sorted(corse_y1)[-2],
            direction=1)
        fine_x3, fine_y3 = self.camera.scan(
            maxsteps=2*course_stepsize, 
            stepsize=1,
            thresh=sorted(fine_y2)[-2],
            direction=-1)
        found = self.camera.find(
            maxsteps=1*course_stepsize, 
            stepsize=1,
            blur_target=min([max(fine_y2), max(fine_y3)]),
            direction=1)
        if found:
            return True 
        else:
            return False
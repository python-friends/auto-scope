from autoscope import Focus


class TestFocus():
    def setup(self):
        self.focus = Focus([9, 10, 11, 12])

    def test_zpins(self):
         assert self.focus.zpins == [9, 10, 11, 12]

    def test_step_z(self):
        self.focus.step_z(nsteps=1000)
        assert self.focus.zpos == 1000 

    def test_goto(self):
        self.focus.goto(-50)
        assert self.focus.zpos == -50

    def test_home(self):
        self.focus.home()
        assert self.focus.zpos == 0

    def test_up(self):
        self.focus.up(10)
        assert self.focus.zpos == 10

    def test_down(self):
        self.focus.down(10)
        assert self.focus.zpos == -10 

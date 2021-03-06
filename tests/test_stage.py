from autoscope import Stage


class TestStage():
    def setup(self):
        self.stage = Stage([1,2,3,4],[5,6,7,8])

    def test_xpins(self):
         assert self.stage.xpins == [1,2,3,4]

    def test_ypins(self):
        assert self.stage.ypins == [5,6,7,8]

    def test_coordinates(self):
        assert self.stage.coordinates == (0, 0)

    def test_step_x(self):
        self.stage.step_x(nsteps=1000)
        assert self.stage.xpos == 1000 

    def test_step_y(self):
        self.stage.step_y(nsteps=-1000)
        assert self.stage.ypos == -1000 

    def test_goto(self):
        self.stage.goto(42, 42)
        assert self.stage.xpos == 42 & self.stage.ypos == 42 

    def test_home(self):
        self.stage.xpos = 42 
        self.stage.ypos = 42
        self.stage.home()
        assert self.stage.xpos == 0 & self.stage.ypos == 0

    def test_set_home(self):
        self.stage.xpos = 42 
        self.stage.ypos = 42
        self.stage.set_home()
        assert self.stage.xpos == 0 & self.stage.ypos == 0

    def test_backward(self):
        self.stage.backward(10)
        assert self.stage.ypos == 10

    def test_forward(self):
        self.stage.forward(20)
        assert self.stage.ypos == -20 

    def test_right(self):
        self.stage.right(10)
        assert self.stage.xpos == 10

    def test_left(self):
        self.stage.left(20)
        assert self.stage.xpos == -20


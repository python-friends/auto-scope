from autoscope.core import step

class TestCore():

    def test_step(self):
        assert step([1,2,3,4], nsteps=-10, speed=1) == -10
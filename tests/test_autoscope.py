import pytest
from autoscope import Autoscope

class TestAutoscope():
    def setup(self):
        self.scope = Autoscope([1,2,3,4],[5,6,7,8],[9,10,11,12])

    def test_stage_attr(self):
        if not hasattr(self.scope, "stage"):
            pytest.fail("Autoscope does not have attribute 'stage'")

    def test_focus_attr(self):
        if not hasattr(self.scope, "focus"):
            pytest.fail("Autoscope does not have attribute 'focus'")

    def test_focus_attr(self):
        if not hasattr(self.scope, "camera"):
            pytest.fail("Autoscope does not have attribute 'camera'")
        
    def test_coordinates(self):
        assert self.scope.coordinates == (0,0,0)
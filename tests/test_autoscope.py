import pytest
from autoscope import Autoscope

class TestAutoscope():
    def setup(self):
        self.scope = Autoscope([1,2,3,4],[5,6,7,8])

    def test_stage_attr(self):
        if not hasattr(self.scope, "stage"):
            pytest.fail("Auto scope does not have attribute 'stage'")
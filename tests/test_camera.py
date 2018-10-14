import pytest
from autoscope import Focus, Camera


class TestAutoscope():
    def setup(self):
        self.camera = Camera(Focus([9,10,11,12]))

    def test_focus_attr(self):
        if not hasattr(self.camera, "focus"):
            pytest.fail("Camera does not have attribute 'focus'")

    
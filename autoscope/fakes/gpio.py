"""
Fake GPIO module
"""
from ..utils import log


class GPIO:
    def __init__(self):
        self.BOARD = 1
        self.OUT = 1
        self.IN = 1
        self.BCM = "BCM"

    def setmode(self, a):
        log.info(a)

    def setup(self, a, b):
        log.info(a)

    def output(self, a, b):
        log.info(a)

    def cleanup(self):
        log.info("clean")

    def setwarnings(self, flag):
        log.info(False)

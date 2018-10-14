"""
Fake GPIO module
"""

class GPIO:
  def __init__(self):
    self.BOARD = 1
    self.OUT = 1
    self.IN = 1
    self.BCM = "BCM"

  def setmode(self, a):
     print(a)
  def setup(self, a, b):
     print(a)
  def output(self, a, b):
     print(a)
  def cleanup(self):
     print('clean')
  def setwarnings(self, flag):
     print(False)

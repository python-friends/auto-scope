"""
Fake GPIO module
wget -N -P RPi/ https://gist.githubusercontent.com/python-friends/b51f4deb7d3e35ff516d1682460c3588/raw/GPIO.py
touch RPi/__init__.py
import RPi.GPIO as GPIO
"""

class GPIO:

  BOARD = 1
  OUT = 1
  IN = 1

  def setmode(self, a):
     print(a)
  def setup(self, a, b):
     print(a)
  def output(self, a, b):
     print(a)
  def cleanup(self):
     print('clean')
  def setmode(self, a):
     print(a)
  def setwarnings(self, flag):
     print(False)

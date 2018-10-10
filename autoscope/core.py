import time
from .utils import log
try:
    import RPi.GPIO as GPIO  # Only works on RPi
except ImportError:
    log.warning("RPi.GPIO not found! Using GPIO test module.")
    from .gpio import GPIO
    GPIO = GPIO()

def step(pins, nsteps, speed=1):
    GPIO.setmode(GPIO.BCM)
    # Set all pins as output
    for pin in pins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, False)

    # halfstep sequence
    halfstep_seq = [
        [1,0,0,1],
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1]]

    sequence_len = len(halfstep_seq)

    if nsteps < 0:
        direction = -1
    else:
        direction = 1

    WaitTime = float(speed)/float(1000)

    StepCounter = 0
    for _ in range(abs(nsteps) * 8): # ensure complete step

        for pin in range(0, 4):
            xpin = pins[pin]
            if halfstep_seq[StepCounter][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        StepCounter += direction

        # If we reach the end of the sequence
        # start again
        if (StepCounter >= sequence_len):
            StepCounter = 0
        if (StepCounter < 0):
            StepCounter = sequence_len + direction

        # Wait before moving on
        time.sleep(WaitTime)
    
    GPIO.cleanup()

    return nsteps

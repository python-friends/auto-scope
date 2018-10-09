from .stage import Stage


class Autoscope:

    def __init__(self, xpins, ypins):
        self.stage = Stage(xpins, ypins)

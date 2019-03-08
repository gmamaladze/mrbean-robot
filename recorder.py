import csv
import time


class Recorder:

    def __init__(self):
        self.start_time = time.time()

    def __del__(self):
        pass

    def create_signal(self, name):
        return Signal(name, self)


class Signal:

    def __init__(self, name, recorder):
        self.name = name
        self.recorder = recorder

    def record(self, value):
        time.time
        pass


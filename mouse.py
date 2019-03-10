import struct
import threading
import logging


class Mouse:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def __enter__(self):
        self.device = open("/dev/input/mice", "rb")
        self.is_stopped = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.get_delta)
        self.thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.is_stopped = True
        self.device.close()

    def read(self):
        self.lock.acquire()
        try:
            dx, dy = self.dx, self.dy
            self.dx, self.dy = 0, 0
        finally:
            self.lock.release()
        return dx, dy

    def get_delta(self):
        logging.debug('Mouse thread entered.')
        while not self.is_stopped:
            buf = self.device.read(3)
            dx, dy = struct.unpack("bb", buf[1:])
            self.lock.acquire()
            try:
                self.dx += dx
                self.dy += dy
            finally:
                self.lock.release()
        logging.debug('Mouse thread exited.')

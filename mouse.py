import struct
import threading


class Mouse:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.device = open("/dev/input/mice", "rb")
        self.is_stopped = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.get_delta)
        self.thread.start()

    def __del__(self):
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
        while not self.is_stopped:
            buf = self.device.read(3)
            dx, dy = struct.unpack("bb", buf[1:])
            self.lock.acquire()
            try:
                self.dx += dx
                self.dy += dy
            finally:
                self.lock.release()

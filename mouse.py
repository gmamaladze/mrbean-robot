import struct
import threading


class Mouse:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.device = open("/dev/input/mice", "rb")
        self.thread = threading.Thread(target=self.get_delta)
        self.thread.start()
        self.lock = threading.Lock()

    def __del__(self):
        self.thread.stop()
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
        while True:
            buf = self.device.read(3)
            dx, dy = struct.unpack("bb", buf[1:])
            self.lock.acquire()
            try:
                self.x += dx
                self.y += dy
            finally:
                self.lock.release()

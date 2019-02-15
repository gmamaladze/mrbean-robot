import struct
import threading


class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.device = open("/dev/input/mice", "rb")
        self.thread = threading.Thread(target=self.get_delta)
        self.thread.start()

    def __del__(self):
        self.thread.stop()
        self.device.close()

    def reset(self):
        self.x = 0
        self.y = 0

    def get_delta(self):
        buf = self.device.read(3)
        # button = ord(buf[0])
        # bLeft = button & 0x1
        # bMiddle = (button & 0x4) > 0
        # bRight = (button & 0x2) > 0
        dx, dy = struct.unpack("bb", buf[1:])
        print(dx, dy)
        self.x += dx
        self.y += dy

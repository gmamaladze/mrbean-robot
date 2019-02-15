import struct


class Mouse:
    def __init__(self):
        self.device = open("/dev/input/mice", "rb")

    def __del__(self):
        self.device.close()

    def get_delta(self):
        buf = self.device.read(3)
        # button = ord(buf[0])
        # bLeft = button & 0x1
        # bMiddle = (button & 0x4) > 0
        # bRight = (button & 0x2) > 0
        dx, dy = struct.unpack("bb", buf[1:])
        return dx, dy

import time
from smbus2 import SMBus

class Light():
    def __init__(self):
        self.BH1750_ADDR = 0x23

    def read_light(self):
        with SMBus(1) as bus:
            b = bus.read_i2c_block_data(self.BH1750_ADDR, 0x10, 2)
            raw = (b[0] << 8) | b[1]
            lux = raw / 1.2
            return lux

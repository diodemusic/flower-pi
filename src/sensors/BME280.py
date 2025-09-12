from smbus2 import SMBus


class Temp:
    def __init__(self, addr=0x76):
        self.ADDR = addr
        self.bus = SMBus(1)

        self.bus.write_byte_data(self.ADDR, 0xF2, 0x01)
        self.bus.write_byte_data(self.ADDR, 0xF4, 0x27)
        self.bus.write_byte_data(self.ADDR, 0xF5, 0xA0)

        self.dig_T1 = self._read_u16(0x88)
        self.dig_T2 = self._read_s16(0x8A)
        self.dig_T3 = self._read_s16(0x8C)

    def _read_u16(self, reg):
        data = self.bus.read_i2c_block_data(self.ADDR, reg, 2)
        return data[0] | (data[1] << 8)

    def _read_s16(self, reg):
        result = self._read_u16(reg)
        if result > 32767:
            result -= 65536
        return result

    def read_temp(self):
        data = self.bus.read_i2c_block_data(self.ADDR, 0xFA, 3)
        raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)

        var1 = (((raw >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (
            ((((raw >> 4) - self.dig_T1) * ((raw >> 4) - self.dig_T1)) >> 12)
            * self.dig_T3
        ) >> 14
        t_fine = var1 + var2
        temp = (t_fine * 5 + 128) >> 8
        return temp / 100.0

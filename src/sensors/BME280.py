from smbus2 import SMBus


class BME280:
    def __init__(self, addr=0x76):
        self.ADDR = addr
        self.bus = SMBus(1)

        self.bus.write_byte_data(self.ADDR, 0xF2, 0x01)
        self.bus.write_byte_data(self.ADDR, 0xF4, 0x27)
        self.bus.write_byte_data(self.ADDR, 0xF5, 0xA0)

        # ---- Temperature calibration
        self.dig_T1 = self._read_u16(0x88)
        self.dig_T2 = self._read_s16(0x8A)
        self.dig_T3 = self._read_s16(0x8C)

        # ---- Pressure calibration
        self.dig_P1 = self._read_u16(0x8E)
        self.dig_P2 = self._read_s16(0x90)
        self.dig_P3 = self._read_s16(0x92)
        self.dig_P4 = self._read_s16(0x94)
        self.dig_P5 = self._read_s16(0x96)
        self.dig_P6 = self._read_s16(0x98)
        self.dig_P7 = self._read_s16(0x9A)
        self.dig_P8 = self._read_s16(0x9C)
        self.dig_P9 = self._read_s16(0x9E)

        # ---- Humidity calibration
        self.dig_H1 = self.bus.read_byte_data(self.ADDR, 0xA1)
        self.dig_H2 = self._read_s16(0xE1)
        self.dig_H3 = self.bus.read_byte_data(self.ADDR, 0xE3)
        e4 = self.bus.read_byte_data(self.ADDR, 0xE4)
        e5 = self.bus.read_byte_data(self.ADDR, 0xE5)
        e6 = self.bus.read_byte_data(self.ADDR, 0xE6)
        self.dig_H4 = (e4 << 4) | (e5 & 0x0F)
        self.dig_H5 = (e6 << 4) | (e5 >> 4)
        self.dig_H6 = self.bus.read_byte_data(self.ADDR, 0xE7)
        if self.dig_H6 > 127:
            self.dig_H6 -= 256

        self._t_fine = 0

    def _read_u16(self, reg):
        data = self.bus.read_i2c_block_data(self.ADDR, reg, 2)
        return data[0] | (data[1] << 8)

    def _read_s16(self, reg):
        result = self._read_u16(reg)
        if result > 32767:
            result -= 65536
        return result

    def _read_raw_data(self):
        """Read raw pressure (3 bytes), temperature (3 bytes), humidity (2 bytes)."""
        data = self.bus.read_i2c_block_data(self.ADDR, 0xF7, 8)
        raw_press = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        raw_temp = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        raw_hum = (data[6] << 8) | data[7]
        return raw_temp, raw_press, raw_hum

    def read_temp(self):
        raw_temp, _, _ = self._read_raw_data()

        var1 = (((raw_temp >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (
            ((((raw_temp >> 4) - self.dig_T1) * ((raw_temp >> 4) - self.dig_T1)) >> 12)
            * self.dig_T3
        ) >> 14
        self._t_fine = var1 + var2
        temp = (self._t_fine * 5 + 128) >> 8
        return temp / 100.0

    def read_pressure(self):
        self.read_temp()
        _, raw_press, _ = self._read_raw_data()

        var1 = self._t_fine - 128000
        var2 = var1 * var1 * self.dig_P6
        var2 = var2 + ((var1 * self.dig_P5) << 17)
        var2 = var2 + (self.dig_P4 << 35)
        var1 = ((var1 * var1 * self.dig_P3) >> 8) + ((var1 * self.dig_P2) << 12)
        var1 = (((1 << 47) + var1) * self.dig_P1) >> 33

        if var1 == 0:
            return 0

        p = 1048576 - raw_press
        p = (((p << 31) - var2) * 3125) // var1
        var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
        var2 = (self.dig_P8 * p) >> 19
        pressure = ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)
        return pressure / 256.0 / 100.0

    def read_humidity(self):
        self.read_temp()
        _, _, raw_hum = self._read_raw_data()

        h = self._t_fine - 76800
        h = (
            (((raw_hum << 14) - (self.dig_H4 << 20) - (self.dig_H5 * h)) + 16384) >> 15
        ) * (
            (
                (
                    (
                        (
                            ((h * self.dig_H6) >> 10)
                            * (((h * self.dig_H3) >> 11) + 32768)
                        )
                        >> 10
                    )
                    + 2097152
                )
                * self.dig_H2
                + 8192
            )
            >> 14
        )
        h = h - (((((h >> 15) * (h >> 15)) >> 7) * self.dig_H1) >> 4)
        h = max(0, min(h, 419430400))
        return (h >> 12) / 1024.0

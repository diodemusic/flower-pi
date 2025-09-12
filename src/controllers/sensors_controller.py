from src.sensors.BH1750 import BH1750
from src.sensors.BME280 import BME280

bh1750 = BH1750()
bme280 = BME280()


def read_sensors():
    light = bh1750.read_light()
    temp = bme280.read_temp()
    pressure = bme280.read_pressure()
    humidity = bme280.read_humidity()

    data = {"light": light, "temp": temp, "pressure": pressure, "humidity": humidity}

    return data

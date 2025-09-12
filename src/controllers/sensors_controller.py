from src.sensors.BH1750 import Light
from src.sensors.BME280 import Temp

light = Light()
temp = Temp()


def read_sensors():
    lux = light.read_light()
    temp_c = temp.read_temp()

    data = {"light": lux, "temp": temp_c}

    return data

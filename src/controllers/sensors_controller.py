from src.sensors.bh1750 import Light

light = Light()


def read_sensors():
    lux = light.read_light()

    data = {
        "light": lux,
    }

    return data

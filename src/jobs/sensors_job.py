import asyncio

from src.database.database import db
from sensors import BH1750  # , BME280

bh1750 = BH1750.BH1750()
# bme280 = BME280.BME280()


async def sensors_job():
    while True:
        light = bh1750.read_light()
        # temp = bme280.read_temp()
        # pressure = bme280.read_pressure()
        # humidity = bme280.read_humidity()

        data = {
            "light": light,
            # "temp": temp,
            # "pressure": pressure,
            # "humidity": humidity,
        }

        db.save_reading(data)
        db.cleanup_old_readings()

        await asyncio.sleep(60)

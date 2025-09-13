import asyncio

import RPi.GPIO as GPIO  # pyright: ignore[reportMissingModuleSource]

from src.database.database import db
from sensors import BH1750, BME280

bh1750 = BH1750.BH1750()
bme280 = BME280.BME280()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)


async def sensors_job():
    is_led_on = False

    while True:
        light = bh1750.read_light()
        temp = bme280.read_temp()
        pressure = bme280.read_pressure()
        humidity = bme280.read_humidity()

        data = {
            "light": light,
            "temp": temp,
            "pressure": pressure,
            "humidity": humidity,
        }
        db.save_reading(data)
        db.cleanup_old_readings()

        if data.get("temp", 0.00) >= 25 and not is_led_on:
            GPIO.output(11, GPIO.HIGH)
            is_led_on = True
        elif data.get("temp", 0.00) < 25 and is_led_on:
            GPIO.output(11, GPIO.LOW)
            is_led_on = False

        await asyncio.sleep(5)

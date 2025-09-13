import os
import asyncio

import RPi.GPIO as GPIO  # pyright: ignore[reportMissingModuleSource]

from src.controllers.sensors_controller import read_sensors
from src.database.database import DB

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "database", "flowerpi.db")
)
db = DB(DB_PATH)
db.init_db()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)


async def sensors_job():
    is_led_on = False

    while True:
        data = read_sensors()
        db.save_reading(data)
        db.cleanup_old_readings()

        if data.get("temp", 0.00) >= 25 and not is_led_on:
            GPIO.output(11, GPIO.HIGH)
            is_led_on = True
        elif data.get("temp", 0.00) < 25 and is_led_on:
            GPIO.output(11, GPIO.LOW)
            is_led_on = False

        await asyncio.sleep(5)

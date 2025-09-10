import os
import asyncio

from src.controllers.sensors_controller import read_sensors
from src.database.database import DB

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "database", "flowerpi.db")
)
db = DB(DB_PATH)
db.init_db()


async def sensor_job():
    while True:
        data = read_sensors()
        db.save_reading(data)
        # cleanup_old_readings(limit=100)
        await asyncio.sleep(5)

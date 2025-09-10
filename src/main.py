from typing import Union
from fastapi import FastAPI
import asyncio

from src.controllers.sensors_controller import read_sensors

from src.jobs.sensors_job import sensor_job

app = FastAPI()


@app.on_event("startup")
async def start_sensor_job():
    await sensor_job()
    asyncio.create_task(sensor_job())


@app.get("/sensors")
def read_sensors_route():
    # Read some entries from the database
    pass

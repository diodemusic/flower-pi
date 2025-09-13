# from typing import Union
from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
import asyncio

from src.controllers.sensors_controller import read_sensors

from src.jobs.sensors_job import sensors_job

app = FastAPI()


@app.on_event("startup")
async def start_jobs():
    asyncio.create_task(sensors_job())


@app.get("/sensors")
def read_sensors_route():
    r = read_sensors()

    return r

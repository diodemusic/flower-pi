import asyncio

from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
# from fastapi.responses import HTMLResponse  # pyright: ignore[reportMissingImports]

from src.controllers.sensors_controller import read_sensors
from src.jobs.sensors_job import sensors_job

app = FastAPI()


@app.on_event("startup")
async def start_jobs():
    asyncio.create_task(sensors_job())


@app.get("/sensors")
def read_sensors_route():
    sensors_data = read_sensors()

    return sensors_data


# @app.get("/dashboard", response_class=HTMLResponse)
# def dashboard():
#     return

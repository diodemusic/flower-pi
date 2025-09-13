import asyncio
from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse  # pyright: ignore[reportMissingImports]
from fastapi.staticfiles import StaticFiles  # pyright: ignore[reportMissingImports]

from src.controllers.sensors_controller import read_sensors
from src.jobs.sensors_job import sensors_job
from src.utils.template import render_template

app = FastAPI()


app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.on_event("startup")
async def start_jobs():
    asyncio.create_task(sensors_job())


@app.get("/sensors")
def read_sensors_route():
    return read_sensors()


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html = render_template("dashboard.html")
    return HTMLResponse(content=html)

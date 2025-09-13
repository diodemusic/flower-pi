import asyncio

from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse  # pyright: ignore[reportMissingImports]

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


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Plant Dashboard</title>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
      <h1>Plant Sensor Dashboard</h1>
      <canvas id="tempChart" width="600" height="300"></canvas>
      <script>
        async function loadData() {
          const res = await fetch('/sensors');
          const data = await res.json();

          // data = [[id, timestamp, light, temp, pressure, humidity], ...]
          const labels = data.map(r => r[1]).reverse();
          const temps = data.map(r => r[3]).reverse();

          const ctx = document.getElementById('tempChart').getContext('2d');
          new Chart(ctx, {
            type: 'line',
            data: {
              labels: labels,
              datasets: [{
                label: 'Temperature (°C)',
                data: temps,
                borderColor: 'red',
                fill: false
              }]
            }
          });
        }
        loadData();
      </script>
    </body>
    </html>
    """

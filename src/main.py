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
      <script src="https://cdn.tailwindcss.com"></script>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <style>
        body {
          background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1600&q=80') no-repeat center center fixed;
          background-size: cover;
        }
        .glass {
          background: rgba(255, 255, 255, 0.15);
          border-radius: 1rem;
          padding: 1rem;
          backdrop-filter: blur(10px);
          box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
          height: 300px; /* Added fixed height */
        }
      </style>
    </head>
    <body class="min-h-screen flex flex-col items-center p-6 text-white">
      <h1 class="text-3xl font-bold mb-6">🌱 Plant Sensor Dashboard</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-6xl">

        <div class="glass">
          <h2 class="text-xl font-semibold mb-2">Light (lux)</h2>
          <canvas id="lightChart"></canvas>
        </div>

        <div class="glass">
          <h2 class="text-xl font-semibold mb-2">Temperature (°C)</h2>
          <canvas id="tempChart"></canvas>
        </div>

        <div class="glass">
          <h2 class="text-xl font-semibold mb-2">Pressure (hPa)</h2>
          <canvas id="pressureChart"></canvas>
        </div>

        <div class="glass">
          <h2 class="text-xl font-semibold mb-2">Humidity (%)</h2>
          <canvas id="humidityChart"></canvas>
        </div>

      </div>

      <script>
        async function loadData() {
          const res = await fetch('/sensors');
          const data = await res.json();

          const labels = data.map(r => r[1]).reverse();
          const light = data.map(r => r[2]).reverse();
          const temp = data.map(r => r[3]).reverse();
          const pressure = data.map(r => r[4]).reverse();
          const humidity = data.map(r => r[5]).reverse();

          const options = { responsive: true, maintainAspectRatio: false };

          new Chart(document.getElementById('lightChart'), {
            type: 'line',
            data: { labels, datasets: [{ label: 'Light', data: light, borderColor: '#fbbf24' }] },
            options
          });

          new Chart(document.getElementById('tempChart'), {
            type: 'line',
            data: { labels, datasets: [{ label: 'Temp', data: temp, borderColor: '#ef4444' }] },
            options
          });

          new Chart(document.getElementById('pressureChart'), {
            type: 'line',
            data: { labels, datasets: [{ label: 'Pressure', data: pressure, borderColor: '#3b82f6' }] },
            options
          });

          new Chart(document.getElementById('humidityChart'), {
            type: 'line',
            data: { labels, datasets: [{ label: 'Humidity', data: humidity, borderColor: '#10b981' }] },
            options
          });
        }

        loadData();
        setInterval(loadData, 10000); // refresh every 10s
      </script>
    </body>
    </html>
    """

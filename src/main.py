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
          background: rgba(34, 197, 94, 0.12);
          border-radius: 1.5rem;
          padding: 1.5rem;
          backdrop-filter: blur(16px);
          border: 1px solid rgba(255, 255, 255, 0.15);
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
          min-height: 320px;
        }
        .chart-title {
          letter-spacing: 0.05em;
          text-shadow: 0 2px 8px rgba(0,0,0,0.18);
        }
        .chart-container {
          height: 220px;
        }
      </style>
    </head>
    <body class="min-h-screen flex flex-col items-center p-6 text-white">
      <h1 class="text-4xl font-extrabold mb-8 drop-shadow-lg">🌱 Plant Sensor Dashboard</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-6xl">

        <div class="glass flex flex-col">
          <h2 class="chart-title text-lg font-semibold mb-2">Light (lux)</h2>
          <div class="chart-container flex-1"><canvas id="lightChart"></canvas></div>
        </div>

        <div class="glass flex flex-col">
          <h2 class="chart-title text-lg font-semibold mb-2">Temperature (°C)</h2>
          <div class="chart-container flex-1"><canvas id="tempChart"></canvas></div>
        </div>

        <div class="glass flex flex-col">
          <h2 class="chart-title text-lg font-semibold mb-2">Pressure (hPa)</h2>
          <div class="chart-container flex-1"><canvas id="pressureChart"></canvas></div>
        </div>

        <div class="glass flex flex-col">
          <h2 class="chart-title text-lg font-semibold mb-2">Humidity (%)</h2>
          <div class="chart-container flex-1"><canvas id="humidityChart"></canvas></div>
        </div>

      </div>

      <script>
        function formatTimeLabel(dateStr) {
          // Format as HH:MM or HH:MM:SS if seconds are not 00
          const d = new Date(dateStr);
          let h = d.getHours().toString().padStart(2, '0');
          let m = d.getMinutes().toString().padStart(2, '0');
          let s = d.getSeconds();
          if (s === 0) {
            return `${h}:${m}`;
          } else {
            s = s.toString().padStart(2, '0');
            return `${h}:${m}:${s}`;
          }
        }

        async function loadData() {
          const res = await fetch('/sensors');
          const data = await res.json();

          const labels = data.map(r => formatTimeLabel(r[1])).reverse();
          const light = data.map(r => r[2]).reverse();
          const temp = data.map(r => r[3]).reverse();
          const pressure = data.map(r => r[4]).reverse();
          const humidity = data.map(r => r[5]).reverse();

          function chartOptions(suffix = "") {
            return {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: false
                },
                tooltip: {
                  callbacks: {
                    label: function(context) {
                      return context.parsed.y + (suffix ? " " + suffix : "");
                    }
                  }
                }
              },
              scales: {
                x: {
                  ticks: { color: '#fff', maxRotation: 0, autoSkip: true, font: { size: 12 } },
                  grid: { display: false }
                },
                y: {
                  ticks: { color: '#fff', font: { size: 12 } },
                  grid: { color: 'rgba(255,255,255,0.08)' }
                }
              }
            };
          }

          // Destroy old charts if they exist to prevent overlay
          window._charts = window._charts || {};
          ['lightChart','tempChart','pressureChart','humidityChart'].forEach(id => {
            if (window._charts[id]) window._charts[id].destroy();
          });

          window._charts.lightChart = new Chart(document.getElementById('lightChart'), {
            type: 'line',
            data: { labels, datasets: [{ label: 'Light', data: light, borderColor: '#fbbf24', backgroundColor: 'rgba(251,191,36,0.15)', fill: true, borderWidth: 2, tension: 0.4, pointRadius: 0 }] },
            options: chartOptions('lux')
          });

          window._charts.tempChart = new Chart(document.getElementById('tempChart'), {
            type: 'line',
            data: { labels, datasets: [{ label: 'Temp', data: temp, borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.15)', fill: true, borderWidth: 2, tension: 0.4, pointRadius: 0 }] },
            options: chartOptions('°C')
          });

          window._charts.pressureChart = new Chart(document.getElementById('pressureChart'), {
            type: 'line',
            data: { labels, datasets: [{ label: 'Pressure', data: pressure, borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.15)', fill: true, borderWidth: 2, tension: 0.4, pointRadius: 0 }] },
            options: chartOptions('hPa')
          });

          window._charts.humidityChart = new Chart(document.getElementById('humidityChart'), {
            type: 'line',
            data: { labels, datasets: [{ label: 'Humidity', data: humidity, borderColor: '#10b981', backgroundColor: 'rgba(16,185,129,0.15)', fill: true, borderWidth: 2, tension: 0.4, pointRadius: 0 }] },
            options: chartOptions('%')
          });
        }

        loadData();
        setInterval(loadData, 10000); // refresh every 10s
      </script>
    </body>
    </html>
    """

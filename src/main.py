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
    const d = new Date(dateStr);
    let h = d.getHours().toString().padStart(2, '0');
    let m = d.getMinutes().toString().padStart(2, '0');
    return `${h}:${m}`;
  }

  // Store chart instances globally
  const chartInstances = {};

  // Define healthy y-axis ranges for each chart
  const yAxisRanges = {
    lightChart:    { min: 0, max: 100 },    // lux: 500-1,000 is good for most plants
    tempChart:     { min: 10, max: 35 },     // °C: 18-30 is healthy for most houseplants
    pressureChart: { min: 950, max: 1050 },  // hPa: typical atmospheric range
    humidityChart: { min: 20, max: 90 }      // %: 40-70% is healthy for most plants
  };

  function chartOptions(suffix = "", chartId = "") {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
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
          min: yAxisRanges[chartId]?.min,
          max: yAxisRanges[chartId]?.max,
          ticks: { color: '#fff', font: { size: 12 } },
          grid: { color: 'rgba(255,255,255,0.08)' }
        }
      }
    };
  }

  async function loadData() {
    const res = await fetch('/sensors');
    const data = await res.json();

    const labels = data.map(r => formatTimeLabel(r[1])).reverse();
    const light = data.map(r => r[2]).reverse();
    const temp = data.map(r => r[3]).reverse();
    const pressure = data.map(r => r[4]).reverse();
    const humidity = data.map(r => r[5]).reverse();

    // Chart configs
    const configs = [
      {
        id: 'lightChart',
        label: 'Light',
        data: light,
        borderColor: '#fbbf24',
        backgroundColor: 'rgba(251,191,36,0.15)',
        suffix: 'lux'
      },
      {
        id: 'tempChart',
        label: 'Temp',
        data: temp,
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239,68,68,0.15)',
        suffix: '°C'
      },
      {
        id: 'pressureChart',
        label: 'Pressure',
        data: pressure,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59,130,246,0.15)',
        suffix: 'hPa'
      },
      {
        id: 'humidityChart',
        label: 'Humidity',
        data: humidity,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16,185,129,0.15)',
        suffix: '%'
      }
    ];

    configs.forEach(cfg => {
      const ctx = document.getElementById(cfg.id).getContext('2d');
      if (!chartInstances[cfg.id]) {
        chartInstances[cfg.id] = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: cfg.label,
              data: cfg.data,
              borderColor: cfg.borderColor,
              backgroundColor: cfg.backgroundColor,
              fill: true,
              borderWidth: 2,
              tension: 0.4,
              pointRadius: 0
            }]
          },
          options: chartOptions(cfg.suffix, cfg.id)
        });
      } else {
        // Update data only
        chartInstances[cfg.id].data.labels = labels;
        chartInstances[cfg.id].data.datasets[0].data = cfg.data;
        chartInstances[cfg.id].options.scales.y.min = yAxisRanges[cfg.id].min;
        chartInstances[cfg.id].options.scales.y.max = yAxisRanges[cfg.id].max;
        chartInstances[cfg.id].update();
      }
    });
  }

  loadData();
  setInterval(loadData, 1000);
</script>
    </body>
    </html>
    """

function formatTimeLabel(dateStr) {
    const d = new Date(dateStr);
    let h = d.getHours().toString().padStart(2, '0');
    let m = d.getMinutes().toString().padStart(2, '0');
    return `${h}:${m}`;
}

const chartInstances = {};

const yAxisRanges = {
    lightChart: { min: 0, max: 20000 },
    tempChart: { min: 10, max: 35 },
    pressureChart: { min: 950, max: 1050 },
    humidityChart: { min: 20, max: 90 }
};

function chartOptions(suffix = "", chartId = "") {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: function (context) {
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

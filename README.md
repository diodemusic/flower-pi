# 🌱 flower-pi

A Raspberry Pi-based plant monitoring system with a real-time dashboard.  
Reads light, temperature, pressure, and humidity from I2C sensors and displays them live in your browser.

---

## 📊 Dashboard

![Dashboard](https://github.com/diodemusic/flower-pi/blob/main/dashboard.png?raw=true)

---

## 🚀 Features

- Real-time sensor readings (light, temperature, pressure, humidity)
- Live dashboard with responsive charts (Chart.js + Tailwind CSS)
- Data storage in SQLite with automatic cleanup
- Easy deployment and startup scripts

---

## 🛠️ Hardware Requirements

- Raspberry Pi (with I2C enabled)
- BH1750 light sensor (I2C)
- BME280 temperature/pressure/humidity sensor (I2C)

---

## ⚡ Installation

Clone the repository:

```bash
git clone https://github.com/diodemusic/flower-pi.git
cd flower-pi/
```

---

## ▶️ Start the API

```bash
./start.sh
```

---

## 🌐 Usage

- Visit `http://<PI_IP>:8000/dashboard` in your browser for the live dashboard.
- The `/sensors` endpoint returns raw sensor data as JSON.

---

## 📝 Notes

- Make sure I2C is enabled on your Pi (`sudo raspi-config` > Interface Options > I2C).
- Adjust healthy chart ranges in the dashboard JS if needed.

---

# 🌦️ Daily Weather Dashboard

An interactive weather dashboard built using [Dash by Plotly](https://dash.plotly.com/) to visualize and explore **1 year of daily weather data for Patna, India**.

This tool allows users to:
- Select custom or quick date ranges
- Toggle between Light and Dark mode
- View interactive temperature, humidity, and condition graphs

---

## 📊 Dataset Overview

- **City**: Patna, India
- **Timeframe**: August 5, 2024 — August 5, 2025
- **Source File**: [`weather_data.csv`](./weather_data.csv)
- **Columns**:
  - `Date` (daily format)
  - `Temperature` (°C)
  - `Humidity` (%)
  - `Condition` (e.g., Clear, Rain)

---

## ⚙️ Installation & Setup


🔁 Clone this Repository

```bash
git clone https://github.com/JagguDada01/Daily-Weather-Dashboard.git
cd Daily-Weather-Dashboard
```

📦 Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
🔧 Install Dependencies
```bash
pip install -r requirements.txt
```
▶️ Run the Application
```bash
python weather.py
```

🌐 Then open your browser and visit:
```
http://127.0.0.1:8050
```
---
## ❗ Trouble? Port Already in Use?

**If you see this error when running the app:**
- Address already in use
- Port 8050 is in use by another program.

✅ Kill the process using port 8050

💻 On macOS/Linux:
```bash
lsof -i :8050
kill -9 <PID>
```
Replace `<PID>` with the number shown in the output of the lsof command.

🖥️ On Windows (Command Prompt):
```bash
netstat -ano | findstr :8050
```
- This will show something like:- **TCP    127.0.0.1:8050   ...   PID: 12345**

**Then stop the process using:**
```bash
taskkill /PID 12345 /F
```
- Replace 12345 with the actual Process ID (PID) shown.

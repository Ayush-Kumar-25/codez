# 🌤️ Weather Forecast Flask Web App

A complete Flask-based Weather Forecast application that uses **OpenWeatherMap API**, **SQLite**, and **PIL** to generate:

- 🌡️ Real-time weather  
- 📅 7-day forecast  
- 🖼️ Auto-generated Weather Images (PNG + PDF)  
- 🗃️ Database storage of forecast results  
- 🔍 Filter & Delete functionality  
- 🌍 Multi-country, multi-city forecasting  
- 🛡️ Secure API key handling using `.env`

---

## 🚀 Features

### ✔ 1. Add Countries and Cities  
User can input:
- Number of countries  
- Each country's name  
- Number of cities in each country  
- Forecast is automatically generated for all cities

### ✔ 2. Weather Forecasting  
Using OpenWeatherMap API:
- 7-day average temperature  
- 7-day average humidity  
- Weather condition  
- Weather icon  
- Stored in SQLite: `weather_forecast.db`

### ✔ 3. Image & PDF Report  
For each forecast date, the app generates:

- `YYYY-MM-DD_Country.png`  
- `YYYY-MM-DD_Country.pdf`  

Each report includes:
- City names  
- Temperatures  
- Humidity  

Rendered using **Pillow (PIL)** with custom fonts (`Inter.ttf`).

### ✔ 4. Web Interface  
Built using Flask with templates:

- `/` – View all forecasts  
- `/filter` – Filter by city  
- `/delete` – Delete city data  
- `/forecast_step1` – Start forecasting wizard  
- `/run_forecast` – Generate forecast  

---

## 🔐 API Key Setup (Safe Method)
- Create a `.env` file (this file is **NOT** pushed to GitHub):
- api_key=YOUR_OPENWEATHERMAP_API_KEY

---

## 🗄️ Database
- SQLite file auto-creates:
- weather_forecast.db

---

## 📦 Installation
1️⃣ Install Dependencies
 - pip install flask requests pillow python-dotenv

2️⃣ Run App
 - python app.py

3️⃣ Visit:
 - http://127.0.0.1:5000/

---

# 🧠 How It Works (Logic Summary)

1. Fetch latitude/longitude from OpenWeatherMap Geo API
2. Fetch 5-day/3-hour forecast
3. Group by date (7 days)
4. Compute:
   - Average temperature
   - Average humidity
   - Most common condition
5. Save to database
6. Generate PNG/PDF report

---

## 🖼️ Screenshots

![alt text](Weather_1.png)
![alt text](Weather_2.png)

---

## 📜 License

- This project is for educational and personal use.


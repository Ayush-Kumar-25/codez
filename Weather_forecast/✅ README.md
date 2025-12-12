✅ README.md (Copy-Paste)
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

---

### ✔ 2. Weather Forecasting  
Using OpenWeatherMap API:
- 7-day average temperature  
- 7-day average humidity  
- Weather condition  
- Weather icon  
- Stored in SQLite: `weather_forecast.db`

---

### ✔ 3. Image & PDF Report  
For each forecast date, the app generates:

- `YYYY-MM-DD_Country.png`  
- `YYYY-MM-DD_Country.pdf`  

Each report includes:
- City names  
- Temperatures  
- Humidity  

Rendered using **Pillow (PIL)** with custom fonts (`Inter.ttf`).

---

### ✔ 4. Web Interface  
Built using Flask with templates:

- `/` – View all forecasts  
- `/filter` – Filter by city  
- `/delete` – Delete city data  
- `/forecast_step1` – Start forecasting wizard  
- `/run_forecast` – Generate forecast  

---

## 🧩 Folder Structure



Weather/
│
├── app.py
├── weather_forecast.db
├── post.png # Base template for weather image
├── Inter.ttf # Font file
├── .env # Stores API key (NOT pushed to GitHub)
├── templates/
│ ├── index.html
│ ├── filter_city.html
│ ├── delete_city.html
│ ├── forecast_step1.html
│ ├── forecast_step2.html
│ ├── forecast_step3.html
│
└── generated_reports/ # PNG and PDF files (optional)


---

## 🔐 API Key Setup (Safe Method)

Create a `.env` file (this file is **NOT** pushed to GitHub):



api_key=YOUR_OPENWEATHERMAP_API_KEY


Load using:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("api_key")

📦 Installation
1️⃣ Install Dependencies
pip install flask requests pillow python-dotenv

2️⃣ Run App
python app.py


Visit:

http://127.0.0.1:5000/

🗄️ Database

SQLite file auto-creates:

weather_forecast.db

🖼️ Screenshots (Add Later)
<img src="screenshot1.png" width="500">
<img src="screenshot2.png" width="500">

🧠 How It Works (Logic Summary)

Fetch latitude/longitude from OpenWeatherMap Geo API

Fetch 5-day/3-hour forecast

Group by date (7 days)

Compute:

Average temperature

Average humidity

Most common condition

Save to database

Generate PNG/PDF report

🤝 Contributing

Pull requests and improvements are welcome!

📄 License

This project is licensed under the MIT License.

👨‍💻 Author

Ayush Kumar
Weather Forecast Flask App
GitHub: your username here
from flask import Flask, render_template, redirect, url_for, request
import json
from datetime import date
import requests
import sqlite3
from PIL import Image, ImageFont, ImageDraw
import os
from dotenv import load_dotenv
from collections import defaultdict, Counter
from datetime import datetime

load_dotenv()
api_key = os.getenv("api_key")
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("weather_forecast.db")
    cursor = conn.cursor()
    cursor.execute('''create table if not exists weather
                   (
                       id integer primary key autoincrement,
                       city text,
                       country text,
                       temperature real,
                       humidity integer,
                       date text,
                       forecast_for_date TEXT,
                       condition TEXT,
                       icon TEXT)
                       ''')
    conn.commit()
    conn.close()

init_db()

def country_code_lookup(country_name):
    country_map = {
        'india': 'IN',
        'united states': 'US',
        'united kingdom': 'GB',
    }
    return country_map.get(country_name.strip().lower(), '')


def forecaster(country_dict):
    conn = sqlite3.connect("weather_forecast.db")
    cursor = conn.cursor()
    
    position = [300, 430, 555, 690, 825]
    for country_name, cities in country_dict.items():
        country_code = country_code_lookup(country_name)

        # Forecast data: forecast_data_by_date[forecast_date] = list of (city, temp, humidity)
        forecast_data_by_date = defaultdict(list)

        for city in cities:
            # Get coordinates
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&limit=1&appid={api_key}"
            geo_response = requests.get(geo_url)
            geo_data = geo_response.json()
            if not geo_data:
                print(f"Geocoding failed for {city}")
                continue
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']

            # Get forecast
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()
            if 'list' not in forecast_data:
                continue

            # Group by forecast date
            daily_data = defaultdict(list)
            for item in forecast_data['list']:
                forecast_date = item['dt_txt'][:10]
                temp = item['main']['temp']
                humidity = item['main']['humidity']
                condition = item['weather'][0]['main']
                icon = item['weather'][0]['icon']
                daily_data[forecast_date].append((temp, humidity, condition, icon))

            for forecast_date, values in list(daily_data.items())[:7]:
                avg_temp = round(sum(t for t, _, _, _ in values) / len(values), 1)
                avg_humidity = round(sum(h for _, h, _, _ in values) / len(values), 1)
                condition_counts = Counter(c for _, _, c, _ in values)
                icon_counts = Counter(ic for _, _, _, ic in values)
                most_common_condition = condition_counts.most_common(1)[0][0]
                most_common_icon = icon_counts.most_common(1)[0][0]

                forecast_data_by_date[forecast_date].append((city.title(), avg_temp, avg_humidity))

                # Insert into DB
                cursor.execute('''
                    INSERT INTO weather (country, city, date, temperature, humidity, forecast_for_date, condition, icon)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (country_name, city, date.today().strftime("%Y-%m-%d"), avg_temp, avg_humidity, forecast_date, most_common_condition, most_common_icon))

        # Create one image per date
        for forecast_date, data_list in forecast_data_by_date.items():
            image = Image.open("post.png")
            draw = ImageDraw.Draw(image)

            font = ImageFont.truetype("Inter.ttf", size=50)
            draw.text((55, 50), "Latest Weather Forecast", "black", font=font)
            
            font = ImageFont.truetype("Inter.ttf", size=30)
            forecast_dt = datetime.strptime(forecast_date, "%Y-%m-%d").strftime("%A - %B %d %Y")
            draw.text((55, 145), forecast_dt, "white", font=font)
            
            for index, (city_name, temp, humidity) in enumerate(data_list[:5]):
                y = position[index]
                font = ImageFont.truetype("Inter.ttf", size=50)
                draw.text((135, y), city_name, "black", font=font)
                font = ImageFont.truetype("Inter.ttf", size=40)
                draw.text((600, y), f"{temp:.2f}°C", "white", font=font)
                font = ImageFont.truetype("Inter.ttf", size=50)
                draw.text((810, y), f"{int(humidity)}%", "white", font=font)
                
            formatted_date = datetime.strptime(forecast_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            filename = f"{formatted_date}_{country_name.title()}.png"
            image.convert("RGB").save(filename)
            image.convert("RGB").save(filename.replace(".png", ".pdf"))

    conn.commit()
    conn.close()
    
def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    return temp, humidity
    
@app.route('/')
def index():
    conn = sqlite3.connect("weather_forecast.db")
    cursor = conn.cursor()
    cursor.execute("select * from weather")
    data = cursor.fetchall()
    conn.close()
    return render_template("index.html", data=data)

@app.route('/filter/', methods = ['GET', 'POST'])
def filter_city():
    result = []
    if request.method == 'POST':
        filter_city = request.form["city"].strip()
        conn = sqlite3.connect("weather_forecast.db")
        cursor = conn.cursor()
        cursor.execute("select * from weather where city = ?", (filter_city,))
        result = cursor.fetchall()
        conn.close()
    return render_template("filter_city.html", data = result)

@app.route('/delete', methods = ['GET', 'POST'])
def delete_city():
        if request.method == 'POST':
            delete_city_name = request.form["city"].strip()
            conn = sqlite3.connect("weather_forecast.db")
            cursor = conn.cursor()
            cursor.execute("delete from weather where city = ?", (delete_city_name,))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
        return render_template("delete_city.html")
    
@app.route('/run_forecast', methods=['GET', 'POST'])
def run_forecast():
    if request.method == 'POST':
        country_dict = {}
        count = int(request.form.get("count"))
        for i in range(count):
            country_name = request.form.get(f"country_{i}")
            city_count = int(request.form.get(f"city_count_{i}"))
            cities = []
            for j in range(city_count):
                city = request.form.get(f"city_{i}_{j}")
                if city:
                    cities.append(city.strip())
            country_dict[country_name] = cities

        forecaster(country_dict)
        return redirect(url_for('index'))
    return redirect(url_for('forecast_step1'))

@app.route('/forecast_step1', methods=['GET', 'POST'])
def forecast_step1():
    if request.method == 'POST':
        count = int(request.form["country_count"])
        return render_template('forecast_step2.html', count=count)
    return render_template('forecast_step1.html')

@app.route('/forecast_step2', methods=['POST'])
def forecast_step2_post():
    country_info = []
    count = int(request.form.get("count"))

    for i in range(count):
        country_name = request.form.get(f"country_{i}")
        city_count = int(request.form.get(f"city_count_{i}"))
        country_info.append({"country": country_name, "city_count": city_count})

    return render_template('forecast_step3.html', country_info=country_info)

@app.route('/forecast_step3', methods=['POST'])
def forecast_step3():
    country_dict = {}
    count = int(request.form.get("count"))
    
    for i in range(count):
        country = request.form.get(f"country_{i}")
        city_count = int(request.form.get(f"city_count_{i}"))
        cities = []
        for j in range(city_count):
            city = request.form.get(f"city_{i}_{j}")
            if city:
                cities.append(city.strip())
        country_dict[country] = cities
    
    forecaster(country_dict)
    return redirect(url_for('index'))

    
if __name__ == "__main__":
    app.run(debug=True)
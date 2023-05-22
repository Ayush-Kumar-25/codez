import requests
import json
from PIL import Image, ImageFont, ImageDraw 
from datetime import date

api_key = "bb64873251675278251c43d380eeb1f5"
position = [300,430,555,690,825]

india_list = ["Hazaribag","Chennai","Delhi","Mumbai","Kolkata"]
uk_list = ["London","Paris","Manchester","Bristol","Birmingham"]
us_list = ["Chicago","New York","San Francisco","Los Angeles","San Diego"]
country_list = [india_list, uk_list, us_list]

for country in country_list:
    image = Image.open("post.png")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("Inter.ttf", size=50)
    content = "Latest Weather Forecast"
    color = "black"
    (x,y) = (55,50)
    draw.text((x, y), content, color, font=font)

    font = ImageFont.truetype("Inter.ttf", size=30)
    content = date.today().strftime("%A - %B %d %Y")
    color = "white"
    (x,y) = (55,145)
    draw.text((x, y), content, color, font=font)

    index = 0
    for city in country:
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&APPID=bb64873251675278251c43d380eeb1f5&units=metric".format(city)
        response = requests.get(url)
        data = json.loads(response.text)
        
        font = ImageFont.truetype("Inter.ttf", size=50)
        color = "black"
        (x,y) = (135,position[index])
        draw.text((x, y), city, color, font=font)
        
        font = ImageFont.truetype("Inter.ttf", size=40)
        content = str(data["main"]["temp"]) + "\u2103"
        color = "white"
        (x,y) = (600,position[index])
        draw.text((x, y), content, color, font=font)

        font = ImageFont.truetype("Inter.ttf", size=50)
        content = str(data["main"]["humidity"]) + "%"
        color = "white"
        (x,y) = (810,position[index])
        draw.text((x, y), content, color, font=font)

        index += 1
        
    image.save(str(date.today()) + country[0] + ".png")
    image_pdf = image.convert("RGB")
    image_pdf.save(str(date.today()) + country[0] + ".pdf")
    
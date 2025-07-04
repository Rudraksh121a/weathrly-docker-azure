from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

# API_KEY = "f7a9acf29f467822e104f95f5a071e91"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    url = "https://api.openweathermap.org/data/2.5/weather"
    API_KEY=request.form.get('api_key')
    print(API_KEY)
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind": data["wind"]["speed"],
            "clouds": data["clouds"]["all"],
            "icon": data["weather"][0]["icon"],
            "sunrise": datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S'),
            "sunset": datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')
        }
        return render_template("weather.html", weather=weather_data)
    else:
        error = data.get("message", "City not found.")
        return render_template("weather.html", error=error, city=city)

if __name__ == '__main__':
    app.run(debug=True)

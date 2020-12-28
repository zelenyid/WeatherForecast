import requests
import datetime

from opencage.geocoder import OpenCageGeocode

from config import OPEN_WEATHER_TOKEN
from config import GEOCODE_TOKEN

URL ='https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude=hourly,daily&appid={API_key}'


class OpenWeatherForecaster:
    @staticmethod
    def current_weather(city):
        weather_url = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city,
                                                                                               OPEN_WEATHER_TOKEN))
        weather_data = weather_url.json()

        curr_weather = {
            'weather': weather_data['weather'][0]['description'].lower(),
            'temp': round(weather_data['main']['temp']),
            'humidity': weather_data['main']['humidity'],
            'wind_speed': round(weather_data['wind']['speed']),
            'wind_degree': round(weather_data['wind']['deg'])
        }

        return curr_weather

    @staticmethod
    def weather_forecast(city):
        geocoder = OpenCageGeocode(GEOCODE_TOKEN)

        results = geocoder.geocode(city)

        weather_url = requests.get(
            'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&units=metric&appid={}'.format(
                results[0]['geometry']['lat'], results[0]['geometry']['lng'],
                OPEN_WEATHER_TOKEN))

        weather_data = weather_url.json()

        forecast = []

        for day in weather_data['daily'][:5]:
            timestamp = datetime.datetime.fromtimestamp(day['dt'])

            forecast.append({
                'date': timestamp.strftime('%Y-%m-%d'),
                'weather': day['weather'][0]['description'].lower(),
                'temp': round(day['temp']['day']),
                'humidity': day['humidity'],
                'wind_speed': round(day['wind_speed']),
                'wind_degree': round(day['wind_deg'])
            })

        return forecast

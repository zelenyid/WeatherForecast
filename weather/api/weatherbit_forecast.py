import requests

from config import WEATHER_BIT_TOKEN


class WeatherBitForecaster:
    @staticmethod
    def current_weather(city):
        weather_url = requests.get(
            'https://api.weatherbit.io/v2.0/current?city={}&key={}'.format(city, WEATHER_BIT_TOKEN))
        weather_data = weather_url.json()

        curr_weather = {
            'weather': weather_data['data'][0]['weather']['description'].lower(),
            'temp': round(weather_data['data'][0]['temp']),
            'humidity': weather_data['data'][0]['rh'],
            'wind_speed': round(weather_data['data'][0]['wind_spd']),
            'wind_degree': round(weather_data['data'][0]['wind_dir'])
        }

        return curr_weather

    @staticmethod
    def weather_forecast(city):
        weather_url = requests.get(
            'https://api.weatherbit.io/v2.0/forecast/daily?city={}&key={}'.format(city, WEATHER_BIT_TOKEN))

        weather_data = weather_url.json()

        forecast = []

        for day in weather_data['data'][:5]:
            forecast.append({
                'date': day['datetime'],
                'weather': day['weather']['description'].lower(),
                'temp': round(day['temp']),
                'humidity': day['rh'],
                'wind_speed': round(day['wind_spd']),
                'wind_degree': round(day['wind_dir'])
            })

        return forecast

import requests

from config import ACCU_WEATHER_TOKEN


class AccuWeatherForecaster:
    @staticmethod
    def current_weather(city):
        location_url = requests.get(
            'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={}&q={}'.format(ACCU_WEATHER_TOKEN, city))
        location_key = location_url.json()[0]['Key']

        weather_url = requests.get(
            'http://dataservice.accuweather.com/currentconditions/v1/{}?apikey={}&details=true'.format(
                location_key, ACCU_WEATHER_TOKEN))
        weather_data = weather_url.json()

        curr_weather = {
            'weather': weather_data[0]['WeatherText'].lower(),
            'temp': round(weather_data[0]['Temperature']['Metric']['Value']),
            'humidity': weather_data[0]['RelativeHumidity'],
            'wind_speed': round(weather_data[0]['Wind']['Speed']['Metric']['Value'] * 5/18),
            'wind_degree': round(weather_data[0]['Wind']['Direction']['Degrees'])
        }

        return curr_weather

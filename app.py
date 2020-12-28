from collections import Counter
from pprint import pprint

from flask import Flask, render_template, request, redirect, url_for

from app.api.open_weather_forecast import OpenWeatherForecaster
from app.api.weatherbit_forecast import WeatherBitForecaster
from app.api.accu_weather_forecast import AccuWeatherForecaster

app = Flask(__name__)


def calculate_probability(*results):
    weathers = []
    temps = []
    humidity = []
    wind_speed = []
    wind_degree = []

    for result in results:
        weathers.append(result['weather'])
        temps.append(result['temp'])
        humidity.append(result['humidity'])
        wind_speed.append(result['wind_speed'])
        wind_degree.append(result['wind_degree'])

    weathers_count = Counter(weathers)
    temps_count = Counter(temps)
    humidity_count = Counter(humidity)
    wind_speed_count = Counter(wind_speed)
    wind_degree_count = Counter(wind_degree)

    percentage_weather = [(weather, round(weathers_count[weather] / len(weathers) * 100.0)) for weather in
                          weathers_count]
    percentage_temps = [(temp, round(temps_count[temp] / len(temps) * 100.0)) for temp in temps_count]
    percentage_humidity = [(hd, round(humidity_count[hd] / len(humidity) * 100.0)) for hd in humidity_count]
    percentage_wind_speed = [(speed, round(wind_speed_count[speed] / len(wind_speed) * 100.0)) for speed in
                             wind_speed_count]
    percentage_wind_degree = [(degree, round(wind_degree_count[degree] / len(wind_degree) * 100.0)) for degree in
                              wind_degree_count]

    return {
        'weather': percentage_weather,
        'temp': percentage_temps,
        'humidity': percentage_humidity,
        'wind_speed': percentage_wind_speed,
        'wind_degree': percentage_wind_degree
    }


@app.route('/forecast_weather/<city>')
def forecast_weather(city):
    forecast_open_weather_map = OpenWeatherForecaster.weather_forecast(city)
    forecast_weather_weather_bit = WeatherBitForecaster.weather_forecast(city)
    # forecast_accuweather = AccuWeatherForecaster.weather_forecast(city)

    probability_weather_forecast = []
    for i in range(len(forecast_open_weather_map)):
        pprint(forecast_open_weather_map)
        date = forecast_open_weather_map[i]['date']
        current_day = calculate_probability(forecast_open_weather_map[i], forecast_weather_weather_bit[i])
        current_day['date'] = date
        probability_weather_forecast.append(current_day)

    return render_template('forecast.html', probability_weather_forecast=probability_weather_forecast, city=city)


@app.route('/current_weather/<city>')
def current_weather(city):
    current_weather_open_weather_map = OpenWeatherForecaster.current_weather(city)
    current_weather_weather_bit = WeatherBitForecaster.current_weather(city)
    current_weather_accuweather = AccuWeatherForecaster.current_weather(city)
    probability_weather = calculate_probability(current_weather_open_weather_map, current_weather_weather_bit, current_weather_accuweather)
    return render_template('result.html', open_weather_map=current_weather_open_weather_map,
                           weather_bit=current_weather_weather_bit,
                           probability_weather=probability_weather, accuweather=current_weather_accuweather, city=city)


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']

    if request.form["action"] == 'current':
        return redirect(url_for('current_weather', city=city))
    elif request.form["action"] == 'forecast':
        return redirect(url_for('forecast_weather', city=city))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('weather.html')


if __name__ == '__main__':
    app.run()

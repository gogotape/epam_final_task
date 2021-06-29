import json
import time

from app_weather.weather_app import WeatherClient


class DemonWeather:
    def do_demon_job(self):
        with open("input/top_100_cities_by_population.json", encoding="utf-8") as fi:
            data = json.load(fi)
            top_100_cities = [item["Name"] for item in data if item["rank"] <= 100]

            for city in top_100_cities:
                try:
                    weather_client = WeatherClient()
                    weather_client.get_city_weather(city, "K")
                except:
                    raise NameError(f"Problem with city named {city}")


while True:
    print("before demon")
    d = DemonWeather()
    d.do_demon_job()
    print("after demon")
    time.sleep(3)

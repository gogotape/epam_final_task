# Create your tasks here


import json

from app_weather.weather_app import WeatherClient
from celery import shared_task

with open("input/top_100_cities_by_population.json", encoding="utf-8") as fi:
    data = json.load(fi)
    top_100_cities = [item["Name"] for item in data if item["rank"] <= 100]


@shared_task
def do_demon_job():
    print("Im working! ***********************************")
    for city in top_100_cities:
        try:
            weather_client = WeatherClient()
            weather_client.get_city_weather(city, "K")
        except:
            raise NameError(f"Problem with city named {city}")

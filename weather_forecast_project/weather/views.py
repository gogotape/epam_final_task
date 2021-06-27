from app_weather.main import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def index(request):
    return HttpResponse(
        "<h1> Welcome to REST API Weather<h1><p>Type your city and units into url string <p>"
        "<h2>"
        "Format: http://127.0.0.1:8000/latin_name_of_city/units (possible units: F, C, K)<h2>"
        "Example: http://127.0.0.1:8000/moscow/F"
    )


def get_weather(request, city, unit):
    # TODO: processing of exceptions
    client = WeatherClient()
    data = client.get_city_weather(city=city, units=unit)
    return JsonResponse(data=data)

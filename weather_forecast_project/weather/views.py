from app_weather.weather_app import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, "templates/base.html")


@login_required
def get_weather(request, city: str, unit: str):
    city.capitalize()
    client = WeatherClient()
    data = client.get_city_weather(city=city, units=unit)
    return JsonResponse(data=data)


@login_required
def save_report(request, from_date, to_date):
    csv_client = SaverInfoClient()
    answer = csv_client.save_data(from_date, to_date)
    return HttpResponse(answer)


def authorize_user(request, username: str, password: str) -> HttpResponse:
    user_client = UserClient()
    answer = user_client.authorize_user(username, password)
    user = authenticate(username=username, password=password)
    login(request=request, user=user)
    return HttpResponse(answer)


def logout_user(request) -> HttpResponse:
    logout(request)
    return HttpResponse("Successfully logout!")

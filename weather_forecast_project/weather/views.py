from app_weather.weather_app import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, "templates/base.html")


@login_required
def get_weather(request, city, unit):
    # TODO: processing of exceptions
    client = WeatherClient()
    data = client.get_city_weather(city=city, units=unit)
    return JsonResponse(data=data)


def authorize_user(request, username, password):
    user_client = UserClient()
    answer = user_client.authorize_user(username, password)
    user = authenticate(username=username, password=password)
    login(request=request, user=user)
    return HttpResponse(answer)


def logout_user(request):
    logout(request)
    return HttpResponse("Successfully logout!")

import json
from datetime import datetime

import requests
from weather.models import *


class WeatherClient:
    # TODO: implement the ability to authenticate
    API_KEY = ""
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    ACCORDANCE = {"K": "standard", "C": "metric", "F": "imperial"}

    def get_city_weather(self, city, units):
        # checking of units, trying to find an accordance of measuring system
        try:
            measuring_system = self.ACCORDANCE[units]
        except Exception as e:
            raise ValueError("Please, type K, C, or F for units")

        # checking availability of data in DB
        if Forecast.objects.filter(
            city=city, units=units, date=datetime.now().date()
        ).exists():
            forecast_obj = Forecast.objects.filter(city=city, units=units)[0]
            data = {
                "city": forecast_obj.city,
                "temperature": forecast_obj.temperature,
                "unit": units,
            }
            return data

        # else going to website to get info
        try:
            params = {"q": city, "units": measuring_system, "appid": self.API_KEY}
            result = requests.get(self.BASE_URL, params=params).json()
            temperature = result["main"]["temp"]
            data = {"city": city, "temperature": temperature, "unit": units}

            # adding data to DB
            Forecast.objects.create(
                city=city,
                date=datetime.now(),
                temperature=float(temperature),
                units=units,
            )
        except KeyError:
            raise KeyError(
                "There is no data about this city. Please, check format of input data"
            )

        return data


class UserClient:
    def authorize_user(self, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                return "User is valid, active and authenticated"
            else:
                return "The password is valid, but the account has been disabled!"
        else:
            # the authentication system was unable to verify the username and password
            return "The username and password were incorrect"

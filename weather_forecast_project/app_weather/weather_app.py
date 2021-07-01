import csv
from datetime import datetime
from typing import Dict

import requests
from weather.models import *


class WeatherClient:
    # TODO: implement the ability to authenticate
    API_KEY = ""
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    ACCORDANCE = {"K": "standard", "C": "metric", "F": "imperial"}

    def get_city_weather(self, city: str, units: str) -> Dict:
        """Getting today's city weather
        Firstly cache is checked, if there is no data for this city and date, then go to website"""
        # checking of units, trying to find an accordance of measuring system
        try:
            measuring_system = self.ACCORDANCE[units]
        except Exception as e:
            raise ValueError("Please, type K, C, or F for units")

        # checking availability of data in DB
        if Forecast.objects.filter(
            city=city, units="K", date=datetime.now().date()
        ).exists():
            forecast_obj = Forecast.objects.filter(city=city, units="K")[0]
            converted_temperature = forecast_obj.convert_temperature(units=units)
            data = {
                "city": forecast_obj.city,
                "temperature": converted_temperature,
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
                f"There is no data about this city: {city}. Please, check format of input data",
            )

        return data


class UserClient:
    @staticmethod
    def authorize_user(username: str, password: str) -> str:
        """Authorize user by username and password"""
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


class SaverInfoClient:
    @staticmethod
    def save_data(from_date, to_date):
        """Save report to csv for some period"""
        try:
            year, month, day = map(int, from_date.split("-"))
            from_date = datetime(year=year, month=month, day=day)
            year1, month1, day1 = map(int, to_date.split("-"))
            to_date = datetime(year=year1, month=month1, day=day1)
        except ValueError:
            raise ValueError("Please, check format of dates")

        data_to_save = list(
            Forecast.objects.filter(date__gte=from_date, date__lte=to_date)
        )
        with open("output/data.csv", "w") as fi:
            for string in data_to_save:
                fi.write(str(string) + "\n")
        if not data_to_save:
            return "There is not data for this period. Check format and values"
        else:
            return "Data successfully saved at /output"

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Forecast(models.Model):
    city = models.CharField(max_length=125)
    date = models.DateField(auto_now=True)
    temperature = models.FloatField()
    units = models.CharField(max_length=30, default="K")

    def __str__(self):
        return "Forecast for {} on {}. Temperature is {} {}".format(
            self.city,
            str(self.date),
            str(self.temperature),
            str(self.units)
        )

    def convert_temperature(self, units: str = "K") -> float:
        if units == "C":
            return float(self.temperature - 273)
        elif units == "F":
            return float(1.8 * (self.temperature - 273) + 32)
        else:
            return float(self.temperature)

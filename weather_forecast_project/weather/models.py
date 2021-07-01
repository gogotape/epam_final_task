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
        return ",".join(
            [str(self.city), str(self.date), str(self.temperature), str(self.units)]
        )

    def convert_temperature(self, units: str = "K") -> float:
        """Convert temperature from K to F and C"""
        if units == "C":
            return round(float(self.temperature - 273))
        elif units == "F":
            return round(float(1.8 * (self.temperature - 273) + 32))
        else:
            return round(float(self.temperature))

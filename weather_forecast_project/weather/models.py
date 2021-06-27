from django.db import models

# Create your models here.


class Forecast(models.Model):
    city = models.CharField(max_length=125)
    date = models.DateTimeField(auto_now=True)
    temperature = models.FloatField()
    units = models.CharField(max_length=30, default="K")

    def __str__(self):
        return "Forecast for {} on {} ".format(
            self.city,
            str(self.date),
        )

    def convert_temperature(self, units="K"):
        if units == "C":
            return self.temperature - 273
        elif units == "F":
            return 1.8 * (self.temperature - 273) + 32
        else:
            return self.temperature

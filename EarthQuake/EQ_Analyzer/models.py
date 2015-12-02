from django.db import models

class EarthQuake(models.Model):
    Origin_Time = models.DateTimeField()
    Magnitude = models.CharField(max_length=200)
    Latitude = models.CharField(max_length=200)
    Longitude = models.CharField(max_length=200)
    Depth = models.CharField(max_length=200)
    Region = models.CharField(max_length=200)


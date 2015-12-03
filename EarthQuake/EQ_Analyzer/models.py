from django.db import models


class EarthQuake(models.Model):

    Origin_Time = models.TextField()
    Magnitude = models.TextField()
    Latitude = models.TextField()
    Longitude = models.TextField()
    Depth = models.TextField()
    Region = models.TextField()


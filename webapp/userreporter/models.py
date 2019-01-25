from django.db import models


class Fire(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    range = models.FloatField()
    is_active = models.BooleanField(default=False)
    probability = models.FloatField(default=0.0)

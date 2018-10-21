from django.db import models

# Create your models here.
class Fire(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    range = models.FloatField()
    is_active = models.BooleanField(default=False)
    probability = models.FloatField(default=0.0)

    class Meta:
        unique_together = (('lat', 'lng'))
from django.db import models


class Station(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)
    longitude = models.DecimalField(decimal_places=3, max_digits=6)
    latitude = models.DecimalField(decimal_places=3, max_digits=6)
    altitude = models.DecimalField(decimal_places=3, max_digits=6)
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code} - {self.name}'

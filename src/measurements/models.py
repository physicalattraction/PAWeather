from django.db import models

from common.utils import datetime_from_day_and_hour
from stations.models import Station, Station


class Measurement(models.Model):
    help_wind_direction = 'Windrichting (in graden) gemiddeld over de laatste 10 minuten van het afgelopen uur ' \
                          '(360=noord, 90=oost, 180=zuid, 270=west, 0=windstil 990=veranderlijk'
    help_wind_speed = 'Uurgemiddelde windsnelheid (in m/s)'
    help_gust_of_wind = 'Hoogste windstoot (in m/s) over het afgelopen uurvak'
    help_temperature = 'Temperatuur (in graden Celsius) op 1.50 m hoogte tijdens de waarneming'
    help_dew_temperature = 'Dauwpuntstemperatuur (in graden Celsius) op 1.50 m hoogte tijdens de waarneming'
    help_sunshine = 'Duur van de zonneschijn (in uren) per uurvak, berekend uit globale straling  ' \
                    '(-1 for <0.05 uur)'
    help_radiation = 'Globale straling (in J/cm2) per uurvak'
    help_precipitation_duration = 'Duur van de neerslag (in uren) per uurvak'
    help_precipitation = 'Uursom van de neerslag (in mm) (-1 voor <0.05 mm)'
    help_air_pressue = 'Luchtdruk (in hPa) herleid naar zeeniveau, tijdens de waarneming'
    help_visibility = 'Horizontaal zicht tijdens de waarneming (0=minder dan 100m, 1=100-200m, 2=200-300m,..., ' \
                      '49=4900-5000m, 50=5-6km, 56=6-7km, 57=7-8km, ..., 79=29-30km, 80=30-35km, 81=35-40km,..., ' \
                      '89=meer dan 70km)'
    help_cloud_cover = 'Bewolking (bedekkingsgraad van de bovenlucht in achtsten), tijdens de waarneming ' \
                       '(9=bovenlucht onzichtbaar)'
    help_relative_humidity = 'Relatieve vochtigheid (in procenten) op 1.50 m hoogte tijdens de waarneming'
    help_mist = 'Mist wel/niet voorgekomen in het voorgaande uur en/of tijdens de waarneming'
    help_rain = 'Regen wel/niet voorgekomen in het voorgaande uur en/of tijdens de waarneming'
    help_snow = 'Sneeuw wel/niet voorgekomen in het voorgaande uur en/of tijdens de waarneming'
    help_lightning = 'Onweer wel/niet voorgekomen in het voorgaande uur en/of tijdens de waarneming'
    help_icing = 'IJsvorming wel/niet voorgekomen in het voorgaande uur en/of tijdens de waarneming'

    decimal_settings = {'decimal_places': 1, 'max_digits': 8, 'null': True, 'blank': True, 'default': None}

    station = models.ForeignKey(Station, related_name='measurements', on_delete=models.CASCADE)
    day = models.DateField()
    hour = models.PositiveSmallIntegerField(blank=True, null=True, default=False)
    time = models.DateTimeField()

    wind_direction = models.DecimalField(help_text=help_wind_direction, **decimal_settings)
    wind_speed = models.DecimalField(help_text=help_wind_speed, **decimal_settings)
    gust_of_wind = models.DecimalField(help_text=help_gust_of_wind, **decimal_settings)
    temperature = models.DecimalField(help_text=help_temperature, **decimal_settings)
    dew_temperature = models.DecimalField(help_text=help_dew_temperature, **decimal_settings)
    sunshine = models.DecimalField(help_text=help_sunshine, **decimal_settings)
    radiation = models.DecimalField(help_text=help_radiation, **decimal_settings)
    precipitation_duration = models.DecimalField(help_text=help_precipitation_duration, **decimal_settings)
    precipitation = models.DecimalField(help_text=help_precipitation, **decimal_settings)
    air_pressure = models.DecimalField(help_text=help_air_pressue, **decimal_settings)
    visibility = models.DecimalField(help_text=help_visibility, **decimal_settings)
    cloud_cover = models.DecimalField(help_text=help_cloud_cover, **decimal_settings)
    relative_humidity = models.DecimalField(help_text=help_relative_humidity, **decimal_settings)

    mist = models.BooleanField(default=False, help_text=help_mist)
    rain = models.BooleanField(default=False, help_text=help_rain)
    snow = models.BooleanField(default=False, help_text=help_snow)
    lightning = models.BooleanField(default=False, help_text=help_lightning)
    icing = models.BooleanField(default=False, help_text=help_icing)

    def save(self, **kwargs):
        if not self.time:
            self.time = datetime_from_day_and_hour(self.day, self.hour)
        return super().save(**kwargs)

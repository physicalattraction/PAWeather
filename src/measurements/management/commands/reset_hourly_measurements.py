import csv
from datetime import datetime
import logging
import os.path

from django.core.management import BaseCommand
from django.db import transaction

from measurements.models import HourlyMeasurement
from stations.models import Station
from utils import data_dir

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Reset the list of measurements based on the input csv file'

    def handle(self, *args, **options):
        hourly_measurements = []
        with open(os.path.join(data_dir, 'hour_knmi.csv'), 'r') as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar=None, skipinitialspace=True)
            for line in csv_reader:
                if line[0].startswith('#'):
                    continue

                line = [value or None for value in line]
                station, day, hour, wind_direction, wind_speed, _, gust_of_wind, temperature, _, dew_temperature, \
                sunshine, radiation, precipitation_duration, precipitation, air_pressure, visibility, cloud_cover, \
                relative_humidity, _, _, mist, rain, snow, lightning, icing = line
                station = Station.objects.get(code=station)
                day = datetime.strptime(day, '%Y%m%d')

                hourly_measurements.append(HourlyMeasurement(
                    station=station, day=day, hour=hour, wind_direction=wind_direction, wind_speed=wind_speed,
                    gust_of_wind=gust_of_wind, temperature=temperature, dew_temperature=dew_temperature,
                    sunshine=sunshine, radiation=radiation, precipitation_duration=precipitation_duration,
                    precipitation=precipitation, air_pressure=air_pressure, visibility=visibility,
                    cloud_cover=cloud_cover, relative_humidity=relative_humidity, mist=mist or False,
                    rain=rain or False, snow=snow or False, lightning=lightning or False, icing=icing or False))

        if not hourly_measurements:
            return

        with transaction.atomic():
            HourlyMeasurement.objects.all().delete()
            HourlyMeasurement.objects.bulk_create(hourly_measurements)
            logger.info('{} hourly measurements processed'.format(len(hourly_measurements)))

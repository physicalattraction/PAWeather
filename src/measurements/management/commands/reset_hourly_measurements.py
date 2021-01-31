import csv
import logging
import os.path
from datetime import datetime

from django.core.management import BaseCommand
from django.db import transaction

from common.utils import data_dir
from data_sources.knmi import DataMode, Knmi
from measurements.models import HourlyMeasurement
from stations.models import Station

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Download the list of hourly measurements from the KNMI, and reset the Database with this information'

    def handle(self, *args, **options):
        data_mode = options['data_mode']
        if data_mode == DataMode.per_day:
            raise NotImplementedError('No model yet for Per Day measurements')

        if options['download']:
            full_path_to_file = Knmi.download_weather(data_mode)
        else:
            full_path_to_file = os.path.join(data_dir, f'per_{data_mode}_knmi.csv')

        hourly_measurements = []
        with open(full_path_to_file, 'r') as f:
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
            logger.info(f'{len(hourly_measurements)}  measurements processed')

    def add_arguments(self, parser):
        help_data_mode = 'Data mode: day or hour'
        parser.add_argument('data_mode', type=str, help=help_data_mode)

        help_download = 'Download the data from the KNMI website before processing'
        parser.add_argument('--download', dest='download', action='store_true', default=False, help=help_download)
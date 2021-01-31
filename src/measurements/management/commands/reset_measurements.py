import csv
import logging
import os.path
from datetime import datetime
from decimal import Decimal
from typing import Optional

from django.core.management import BaseCommand
from django.db import transaction

from common.utils import data_dir, datetime_from_day_and_hour
from data_sources.knmi import DataMode, Knmi
from measurements.models import Measurement
from stations.models import Station

logger = logging.getLogger(__name__)


def parse_knmi_number(n: Optional[str]) -> Optional[Decimal]:
    """
    Parse the Knmi numbers that are measured in 0.1 of a unit

    :param n: String representation of the Knmi csv file
    :return: Decimal representing that number

    >>> parse_knmi_number('24')
    2.4
    >>> parse_knmi_number(None)
    None
    """

    if n is None:
        return None
    return Decimal(n) / 10


class Command(BaseCommand):
    help = 'Download the list of hourly measurements from the KNMI, and reset the Database with this information'

    def handle(self, *args, **options):
        data_mode = DataMode(options['data_mode'])
        if data_mode == DataMode.per_day:
            raise NotImplementedError('No model yet for Per Day measurements')

        if options['download']:
            print('Downloading hourly measurements')
            full_path_to_file = Knmi.download_weather(data_mode)
        else:
            full_path_to_file = os.path.join(data_dir, f'{data_mode.name}_knmi.csv')

        # TODO: Move this to a dedicated importer, instead of in a Django command
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

                hourly_measurements.append(Measurement(
                    station=station, day=day, hour=hour, time=datetime_from_day_and_hour(day, int(hour) - 1),
                    wind_direction=parse_knmi_number(wind_direction),
                    wind_speed=parse_knmi_number(wind_speed), gust_of_wind=parse_knmi_number(gust_of_wind),
                    temperature=parse_knmi_number(temperature), dew_temperature=parse_knmi_number(dew_temperature),
                    sunshine=parse_knmi_number(sunshine), radiation=radiation,
                    precipitation_duration=parse_knmi_number(precipitation_duration),
                    precipitation=parse_knmi_number(precipitation), air_pressure=parse_knmi_number(air_pressure),
                    visibility=visibility, cloud_cover=cloud_cover, relative_humidity=relative_humidity,
                    mist=mist or False, rain=rain or False, snow=snow or False, lightning=lightning or False,
                    icing=icing or False)
                )

        if not hourly_measurements:
            return

        with transaction.atomic():
            Measurement.objects.all().delete()
            Measurement.objects.bulk_create(hourly_measurements)
            logger.info(f'{len(hourly_measurements)}  measurements processed')

    def add_arguments(self, parser):
        help_data_mode = 'Data mode: day or hour'
        parser.add_argument('data_mode', type=str, help=help_data_mode)

        help_download = 'Download the data from the KNMI website before processing'
        parser.add_argument('--download', dest='download', action='store_true', default=False, help=help_download)

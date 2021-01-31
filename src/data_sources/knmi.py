import csv
import logging
import os.path
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

import requests
from django.db import transaction

from common.utils import data_dir, datetime_from_day_and_hour
from measurements.models import Measurement
from stations.models import Station

logger = logging.getLogger(__name__)


class DownloadException(Exception):
    pass


class DataMode(Enum):
    per_day = 'day'
    per_hour = 'hour'


class Knmi:
    URLS = {
        DataMode.per_day: 'http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi',
        DataMode.per_hour: 'http://projects.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi',
    }

    @staticmethod
    def download_weather(data_mode: DataMode, start: str = None, end: str = None, stations: str = 'ALL') -> str:
        """
        Download the data from the KNMI website and store them in a csv file in the data directory

        :param data_mode: Download per day or per hour
        :param start: string YYYYMMDD(HH) for start time
        :param end: string YYYYMMDD(HH) for end time
        :param stations: string with : separated station codes.
                         TODO: Implement the per-station download
        :return: Full path to generated file
        """

        # Input validation
        if data_mode not in Knmi.URLS:
            known_data_modes = ', '.join([mode.name for mode in DataMode])
            msg = f'Unknown data mode {data_mode}. Choose from: {known_data_modes}'
            raise AssertionError(msg)

        # Determine query parameters
        data = {'stns': 'ALL'}
        if start:
            data['start'] = start
        if end:
            data['end'] = end
        # TODO: Remove this start date which is here for testing purposes only
        data['start'] = '2021012801'

        # Make the request
        response = requests.get(url=Knmi.URLS[data_mode], params=data)
        if response.status_code != 200:
            msg = response.text
            raise DownloadException(msg)

        # Write the response to file
        filename = f'{data_mode.name}_knmi.csv'
        full_path_to_file = os.path.join(data_dir, filename)
        with open(full_path_to_file, 'w') as f:
            f.write(response.text)
        logger.info(f'Weather information {data_mode.name} has been downloaded to {full_path_to_file}')
        return full_path_to_file

    @staticmethod
    def import_weather(data_mode: DataMode, full_path_to_file: str) -> List[Measurement]:
        assert data_mode == DataMode.per_hour, 'Measurements per day not yet implemented'

        hourly_measurements = []
        stations = {station.code: station for station in Station.objects.all()}
        with open(full_path_to_file, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar=None, skipinitialspace=True)
            for line in csv_reader:
                if line[0].startswith('#'):
                    continue

                line = [value or None for value in line]
                station_code, day, hour, wind_direction, wind_speed, _, gust_of_wind, temperature, _, dew_temperature, \
                sunshine, radiation, precipitation_duration, precipitation, air_pressure, visibility, cloud_cover, \
                relative_humidity, _, _, mist, rain, snow, lightning, icing = line
                station = stations[station_code]
                day = datetime.strptime(day, '%Y%m%d')

                hourly_measurements.append(Measurement(
                    station=station, day=day, hour=hour, time=datetime_from_day_and_hour(day, int(hour) - 1),
                    wind_direction=Knmi._parse_number(wind_direction),
                    wind_speed=Knmi._parse_number(wind_speed), gust_of_wind=Knmi._parse_number(gust_of_wind),
                    temperature=Knmi._parse_number(temperature), dew_temperature=Knmi._parse_number(dew_temperature),
                    sunshine=Knmi._parse_number(sunshine), radiation=radiation,
                    precipitation_duration=Knmi._parse_number(precipitation_duration),
                    precipitation=Knmi._parse_number(precipitation), air_pressure=Knmi._parse_number(air_pressure),
                    visibility=visibility, cloud_cover=cloud_cover, relative_humidity=relative_humidity,
                    mist=mist or False, rain=rain or False, snow=snow or False, lightning=lightning or False,
                    icing=icing or False)
                )

        if not hourly_measurements:
            return []

        with transaction.atomic():
            Measurement.objects.all().delete()
            Measurement.objects.bulk_create(hourly_measurements)
        return hourly_measurements

    @staticmethod
    def _parse_number(n: Optional[str]) -> Optional[Decimal]:
        """
        Parse the Knmi numbers that are measured in 0.1 of a unit

        :param n: String representation of the Knmi csv file
        :return: Decimal representing that number

        >>> Knmi._parse_number('24')
        2.4
        >>> Knmi._parse_number(None)
        None
        """

        if n is None:
            return None
        return Decimal(n) / 10

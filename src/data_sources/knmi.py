import logging
import os.path
from enum import Enum

import requests

from common.utils import data_dir

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


if __name__ == '__main__':
    result = Knmi.download_weather(DataMode.per_day)

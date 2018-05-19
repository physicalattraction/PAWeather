import os.path

import requests

from utils import data_dir


class DownloadException(Exception):
    pass


class Knmi:
    DATA_MODE_DAY = 'day'
    DATA_MODE_HOUR = 'hour'
    URLS = {
        DATA_MODE_DAY: 'http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi',
        DATA_MODE_HOUR: 'http://projects.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi',
    }

    def download_weather(self, data_mode: str, start: str = None, end: str = None, stations: str = 'ALL'):
        """
        Download the data from the KNMI website and store them in a csv file in the data directory

        :param data_mode: Download per day or per hour
        :param start: string YYYYMMDD(HH) for start time
        :param end: string YYYYMMDD(HH) for end time
        :param stations: string with : separated station codes
        """

        # Input validation
        if data_mode not in self.URLS:
            msg = 'Unknown data mode {}. Choose from: {}'.format(data_mode, ', '.join(self.URLS.keys()))
            raise AssertionError(msg)

        # Determine query parameters
        data = {'stns': 'ALL'}
        if start:
            data['start'] = start
        if end:
            data['end'] = end

        # Make the request
        response = requests.get(url=self.URLS[data_mode], params=data)
        if response.status_code != 200:
            msg = response.text
            raise DownloadException(msg)

        # Write the response to file
        filename = '{}_knmi.csv'.format(data_mode)
        with open(os.path.join(data_dir, filename), 'w') as f:
            f.write(response.text)


if __name__ == '__main__':
    knmi = Knmi()
    result = knmi.download_weather()

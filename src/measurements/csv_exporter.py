import csv
import os.path

from common.utils import data_dir
from measurements.models import Measurement


class CsvExporter:
    @staticmethod
    def export():
        """
        Export the given range of measurements to a csv file, usable by Google Data Studio
        """

        # TODO: Google Data Studio has a Latitude,Longitude field. Check out what it expects and export it as such

        station_fields = ['code', 'name', 'longitude', 'latitude', 'altitude']
        measurement_fields = ['time', 'wind_direction', 'wind_speed', 'gust_of_wind', 'temperature',
                              'dew_temperature', 'sunshine', 'radiation', 'precipitation_duration', 'precipitation',
                              'air_pressure', 'visibility', 'cloud_cover', 'relative_humidity', 'mist', 'rain', 'snow',
                              'lightning', 'icing']
        q = Measurement.objects.all().prefetch_related('station').values_list(
            *[f'station__{field}' for field in station_fields], *measurement_fields
        )

        filename = 'per_hour_weather.csv'
        full_path_to_file = os.path.join(data_dir, filename)
        with open(full_path_to_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(station_fields + measurement_fields)
            for measurement in q:
                writer.writerow(measurement)

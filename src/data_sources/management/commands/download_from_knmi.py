from django.core.management import BaseCommand

from data_sources.knmi import DataMode, Knmi


class Command(BaseCommand):
    help = 'Download the weather measurements from the KNMI'

    def handle(self, *args, **options):
        full_path_to_file = Knmi.download_weather(DataMode.per_hour)
        measurements = Knmi.import_weather(DataMode.per_hour, full_path_to_file)
        print(f'Successfully downloaded and imported {full_path_to_file}, '
              f'resulting in {len(measurements)} measurements')

    def add_arguments(self, parser):
        help_data_mode = 'Data mode: day or hour'
        parser.add_argument('data_mode', type=str, help=help_data_mode)

from django.core.management import BaseCommand

from data_sources.knmi import DataMode, Knmi


class Command(BaseCommand):
    help = 'Download the weather measurements from the KNMI'

    def handle(self, *args, **options):
        knmi = Knmi()
        full_path_to_file = knmi.download_weather(data_mode=DataMode.per_hour)
        print(f'Successfully downloaded {full_path_to_file}')

    def add_arguments(self, parser):
        help_data_mode = 'Data mode: day or hour'
        parser.add_argument('data_mode', type=str, help=help_data_mode)

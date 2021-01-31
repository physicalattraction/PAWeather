import logging

from django.core.management import BaseCommand

from data_sources.knmi import DataMode
from measurements.csv_exporter import CsvExporter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Export the list of hourly measurements'

    def handle(self, *args, **options):
        data_mode = DataMode(options['data_mode'])
        if data_mode == DataMode.per_day:
            raise NotImplementedError('No model yet for Per Day measurements')

        CsvExporter.export()

    def add_arguments(self, parser):
        help_data_mode = 'Data mode: day or hour'
        parser.add_argument('data_mode', type=str, help=help_data_mode)

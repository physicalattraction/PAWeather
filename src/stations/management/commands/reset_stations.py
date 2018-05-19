import csv
import logging
import os.path

from django.core.management import BaseCommand
from django.db import transaction

from stations.models import Station
from utils import data_dir

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Reset the list of stations based on the input csv file'

    def handle(self, *args, **options):
        stations = []
        with open(os.path.join(data_dir, 'stations.csv'), 'r') as f:
            Station.objects.all().delete()
            csv_reader = csv.reader(f, delimiter=' ', quotechar=None, skipinitialspace=True)
            for line in csv_reader:
                code, lon, lat, alt = line[1:4 + 1]
                name = ' '.join(line[5:]).capitalize()
                code = code[:3]  # Strip the colon after the station code
                stations.append(Station(code=code, longitude=lon, latitude=lat, altitude=alt, name=name))

        if not stations:
            return

        with transaction.atomic():
            Station.objects.all().delete()
            Station.objects.bulk_create(stations)
            logger.info('{} stations processed'.format(len(stations)))

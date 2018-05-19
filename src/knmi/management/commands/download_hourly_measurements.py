import logging

from django.core.management import BaseCommand

from knmi.knmi import Knmi


class Command(BaseCommand):
    help = 'Reset the list of measurements based on the input csv file'

    def handle(self, *args, **options):
        knmi = Knmi()
        knmi.download_weather(data_mode=knmi.DATA_MODE_HOUR)

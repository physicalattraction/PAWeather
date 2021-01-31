import os.path
from datetime import date, datetime
from typing import Optional

import pytz
from django.utils import timezone

src_dir = os.path.dirname(os.path.dirname(__file__))
root_dir = os.path.dirname(src_dir)
data_dir = os.path.join(root_dir, 'data')


def datetime_from_day_and_hour(day: date, hour: Optional[int],
                               tz: timezone = pytz.utc) -> datetime:
    """
    Convert a date and optionally an hour and a timezone into a timezone-aware datetime object
    """

    return timezone.datetime(day.year, day.month, day.day, hour=hour, tzinfo=tz)

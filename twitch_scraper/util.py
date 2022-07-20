import datetime

from dateutil import parser as dateparser


def date_to_RFC3339(date: datetime.datetime):
    return date.isoformat() + "Z"

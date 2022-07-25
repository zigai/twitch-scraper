import datetime


def date_to_RFC3339(date: datetime.datetime):
    return date.isoformat() + "Z"

import datetime


def date_to_rfc3339(date: datetime.datetime):
    return date.isoformat() + "Z"

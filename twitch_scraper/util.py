from datetime import datetime


def date_to_rfc3339(date: datetime) -> str:
    return date.isoformat() + "Z"

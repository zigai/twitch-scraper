from __future__ import annotations

from datetime import datetime
from typing import TypeAlias

JsonValue: TypeAlias = bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"] | None


def date_to_rfc3339(date: datetime) -> str:
    """Convert a datetime to an RFC 3339 UTC timestamp string."""
    return date.isoformat() + "Z"

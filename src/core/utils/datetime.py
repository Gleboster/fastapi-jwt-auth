from datetime import datetime, timezone

_tz = timezone.utc

def datetime_now():
    return datetime.now(tz=_tz)

def datetime_fromtimestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=_tz)
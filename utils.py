from datetime import datetime
import pytz


LOCALTIME = pytz.timezone("Asia/Ho_Chi_Minh")


def naive_to_aware(dt: datetime):
    """
    Converts naive datetime to aware datetime.
    """
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt


def dt_to_local(dt: datetime):
    """
    Converts aware datetime to local datetime.
    """
    return LOCALTIME.normalize(naive_to_aware(dt))

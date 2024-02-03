import pytz
from datetime import datetime, timedelta, time, tzinfo

from src.db.conn import async_session
from src.db import models


def execute() -> None:
    obj = models.Person(
        datetime_camel_timezone_true=datetime.utcnow(),
        datetime_camel_timezone_false=datetime.utcnow(),
        date_camel=datetime.utcnow(),
        date_upper=datetime.utcnow(),
        time_camel_timezone_false=time(hour=10, minute=12, second=30),
        time_camel_timezone_true=time(hour=10, minute=12, second=30, tzinfo=pytz.utc),
        time_upper_timezone_false=time(hour=10, minute=12, second=30),
        time_upper_timezone_true=time(hour=10, minute=12, second=30, tzinfo=pytz.utc),
        timestamp_upper_timezone_false=datetime.utcnow(),
        timestamp_upper_timezone_true=datetime.utcnow(),
        interval_camel_native_true=timedelta(days=10),
        interval_camel_native_false=timedelta(days=10),
    )
    with async_session() as session:
        session.add(obj)
        session.commit()

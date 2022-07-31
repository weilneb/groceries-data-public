from datetime import datetime
from typing import Optional

from peewee import DoesNotExist

from app.db import Schedule, ScheduleStatus


def get_next_to_scrape() -> Optional[Schedule]:
    try:
        return Schedule.select().where(
            (Schedule.status == ScheduleStatus.SCHEDULED)
        ).order_by(
            Schedule.scheduled_for.asc()
        ).limit(1).get()
    except DoesNotExist:
        pass


def get_sleep_seconds(min_sleep_seconds=15) -> int:
    next_to_run = get_next_to_scrape()
    if next_to_run:
        delta = next_to_run.scheduled_for - datetime.now()
        seconds = delta.total_seconds()
        return max(seconds, min_sleep_seconds)
    else:
        return min_sleep_seconds

import datetime

import pytest

from app.db import get_all_schedules, Schedule, Product, get_all_products, ScheduleStatus
from app import scheduler


@pytest.mark.usefixtures("test_db")
class TestGetNextScheduled:
    def test_when_future_scheduled_exists(self):
        product = Product.create(url='http://a.com', category='a')

        five_days_in_future = datetime.datetime.now() + datetime.timedelta(days=5)
        Schedule.create(product=product,
                        scheduled_for=five_days_in_future)

        five_hours_in_future = datetime.datetime.now() + datetime.timedelta(hours=5)
        scheduled_in_five_hours = Schedule.create(product=product,
                                                  scheduled_for=five_hours_in_future)

        assert scheduled_in_five_hours.status == ScheduleStatus.SCHEDULED
        assert len(get_all_products()) == 1
        assert len(get_all_schedules()) == 2

        assert scheduler.get_next_to_scrape() == scheduled_in_five_hours
        # TODO: better way to test this?
        assert abs(scheduler.get_sleep_seconds(min_sleep_seconds=10) - datetime.timedelta(hours=5).total_seconds()) < 10

    def test_when_no_future_scheduled_exists(self):
        product = Product.create(url='http://a.com', category='a')
        Schedule.create(product=product, status=ScheduleStatus.SUCCESS)
        Schedule.create(product=product, status=ScheduleStatus.FAILED)

        assert len(get_all_schedules()) == 2

        assert scheduler.get_next_to_scrape() is None
        assert scheduler.get_sleep_seconds(min_sleep_seconds=60) == 60

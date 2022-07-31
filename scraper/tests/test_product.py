import datetime

import pytest

from app.db import Product, ScheduleStatus, get_all_products, get_all_schedules
from app.product import insert_and_schedule_product_if_not_exists
from app.product_info import ProductInfo


def test_create_product(test_db):
    assert len(get_all_products()) == 0
    p1 = Product.create(url='http://a.com', category='a')
    p2 = Product.create(url='http://b.com', category='b')
    products = get_all_products()
    assert set(products) == {p1, p2}


@pytest.mark.usefixtures("test_db")
class TestInsertAndScheduleProduct:
    def test_insert_when_not_exists(self):
        assert get_all_products() == []
        assert get_all_schedules() == []

        pi = ProductInfo(url='http://a.com/milk', category='milk')
        insert_and_schedule_product_if_not_exists(pi)

        products = get_all_products()
        assert len(products) == 1
        saved_product = products[0]
        assert saved_product.url == pi.url

        schedules = get_all_schedules()
        saved_schedule = schedules[0]
        assert saved_schedule.status == ScheduleStatus.SCHEDULED
        assert saved_schedule.scheduled_for < datetime.datetime.now()
        assert saved_schedule.product == saved_product

    def test_dont_insert_when_already_exists(self):
        pi = ProductInfo(url='http://a.com/milk', category='milk')
        Product.create(url=pi.url, category=pi.category)
        assert len(get_all_products()) == 1
        assert Product.get(Product.url == pi.url) is not None
        assert len(get_all_schedules()) == 0

        insert_and_schedule_product_if_not_exists(pi)
        assert len(get_all_products()) == 1
        assert len(get_all_schedules()) == 0

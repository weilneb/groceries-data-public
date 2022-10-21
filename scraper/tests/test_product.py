import datetime

import pytest

from app.db import Product, ScheduleStatus, get_all_products, get_all_schedules
from app.product import upsert_product, update_products
from app.product_info import ProductInfo


def test_create_product(test_db):
    assert len(get_all_products()) == 0
    p1 = Product.create(name='A', url='http://a.com', category='a')
    p2 = Product.create(name='B', url='http://b.com', category='b')
    products = get_all_products()
    assert set(products) == {p1, p2}


def test_update_products_and_disable_any_missing(test_db):
    Product.create(name='Bread', url='http://a.com/bread', category='bread')
    milk_pi = ProductInfo(name='Milk', url='http://a.com/milk', category='milk')

    update_products([milk_pi])

    products = get_all_products()
    assert len(products) == 2

    milk_saved = Product.get(Product.name == 'Milk')
    assert milk_saved.enabled

    bread_saved = Product.get(Product.name == 'Bread')
    assert not bread_saved.enabled


@pytest.mark.usefixtures("test_db")
class TestUpsertProduct:
    def test_insert_when_not_exists(self):
        assert get_all_products() == []
        assert get_all_schedules() == []

        pi = ProductInfo(url='http://a.com/milk', category='milk', name='Milk')
        upsert_product(pi)

        products = get_all_products()
        assert len(products) == 1
        saved_product = products[0]
        assert saved_product.url == pi.url
        assert saved_product.name == pi.name
        assert saved_product.category == pi.category

        schedules = get_all_schedules()
        saved_schedule = schedules[0]
        assert saved_schedule.status == ScheduleStatus.SCHEDULED
        assert saved_schedule.scheduled_for < datetime.datetime.now()
        assert saved_schedule.product == saved_product

    def test_update_details_when_already_exists(self):
        pi = ProductInfo(url='http://a.com/milk', category='milk', name='Milk')
        Product.create(name=pi.name, url=pi.url, category=pi.category, enabled=False)
        assert len(get_all_products()) == 1
        assert Product.get(Product.name == 'Milk') is not None
        assert len(get_all_schedules()) == 0

        pi.url = 'http://b.com/milk'
        upsert_product(pi)
        products = get_all_products()
        assert len(products) == 1

        saved_product = products[0]
        assert saved_product.url == pi.url
        assert saved_product.name == pi.name
        assert saved_product.category == pi.category
        assert saved_product.enabled

        assert len(get_all_schedules()) == 0

import logging
from typing import List

from peewee import DoesNotExist

from app.product_info import ProductInfo
from app.db import Product, Schedule

logger = logging.getLogger(__name__)


def insert_and_schedule_product_if_not_exists(prod: ProductInfo):
    try:
        Product.get(Product.url == prod.url)
    except DoesNotExist:
        p = Product.create(url=prod.url, category=prod.category)
        Schedule.create(product=p)
    else:
        logger.info(f"Product {prod} already exists in db.")


def insert_products(products: List[ProductInfo]):
    for prod in products:
        insert_and_schedule_product_if_not_exists(prod)

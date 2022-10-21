import logging
from typing import List

from peewee import DoesNotExist

from app.product_info import ProductInfo
from app.db import Product, Schedule

logger = logging.getLogger(__name__)


def upsert_product(prod: ProductInfo):
    """
    If product does not exist:
        - insert it & schedule
    If product already exists:
        - update the url
        - set status to enabled
    """
    try:
        existing_product = Product.get(Product.name == prod.name)
        # TODO: if url is different and last schedule failed
        #  then immediately schedule a scrape
        existing_product.url = prod.url
        existing_product.enabled = True
        existing_product.save()
        logger.info(f"Updated Product: {existing_product}.")
    except DoesNotExist:
        logger.info(f"Creating Product: {prod}.")
        p = Product.create(name=prod.name, url=prod.url, category=prod.category)
        Schedule.create(product=p)


def disable_products_not_in_list(products: List[ProductInfo]):
    product_names_enabled = {p.name for p in products}
    all_existing_product_names = {p.name for p in Product.select()}
    to_disable = all_existing_product_names.difference(product_names_enabled)
    logger.info(f"Disabling products: {to_disable}")

    # disable any products not present in list
    for prod in Product.select().where(Product.name.in_(to_disable)):
        prod.enabled = False
        prod.save()


def update_products(products: List[ProductInfo]):
    for prod in products:
        upsert_product(prod)
    disable_products_not_in_list(products)

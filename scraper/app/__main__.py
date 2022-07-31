import logging
import os.path
import time
from datetime import datetime, timedelta
from typing import List

import yaml

from app.db import create_tables, Product, Schedule, ScheduleStatus, list_all_products, list_all_schedule
from app.product import insert_products
from app.product_info import ProductInfo
from app.scheduler import get_next_to_scrape, get_sleep_seconds
from app.scraper import get_product_price
from app.sns import publish_to_sns
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MIN_SLEEP_SECONDS_BETWEEN_SCRAPES = int(os.getenv('SECONDS_BETWEEN_SCRAPES', 15))
logger.info(f'SECONDS_BETWEEN_SCRAPES={MIN_SLEEP_SECONDS_BETWEEN_SCRAPES}')


# TODO: move to another file
def get_products_from_file(filepath: str) -> List[ProductInfo]:
    with open(filepath) as f:
        obj = yaml.load(f, Loader=yaml.FullLoader)['products']
        products = []
        for category in obj:
            for url in category['urls']:
                products.append(ProductInfo(url=url, category=category['category']))

        return products


class Poller:

    def __init__(self, scraping_period: timedelta = timedelta(days=1)):
        self.scraping_period = scraping_period

    def poll(self):
        while True:
            logger.info("Polling...")
            list_all_schedule()
            next_to_run = get_next_to_scrape()
            if next_to_run and next_to_run.scheduled_for <= datetime.now():
                logger.info(f"Scraping for: schedule={next_to_run}")
                self.scrape_product(scheduled_job=next_to_run)
            self.sleep()

    # TODO: test coverage.
    def scrape_product(self, scheduled_job: Schedule):
        product = scheduled_job.product
        try:
            product_dto = get_product_price(url=product.url, category=product.category)

            publish_to_sns(product_dto.to_json())

            scheduled_job.status = ScheduleStatus.SUCCESS
            scheduled_job.save()

        # TODO: scraper -> throw a custom exception, maybe called ProductOutOfStock
        except TimeoutException:
            logger.exception(f'Product [{product}] may be out-of-stock.')
            scheduled_job.status = ScheduleStatus.FAILED
            scheduled_job.save()
        finally:
            self.schedule_next_scraping(product=product)

    def schedule_next_scraping(self, product: Product):
        datetime_future = datetime.now() + self.scraping_period
        Schedule.create(product=product, scheduled_for=datetime_future)

    @staticmethod
    def sleep():
        min_sleep_secs = get_sleep_seconds(min_sleep_seconds=MIN_SLEEP_SECONDS_BETWEEN_SCRAPES)
        logger.info(f"Sleeping for {min_sleep_secs} seconds")
        time.sleep(min_sleep_secs)


if __name__ == '__main__':
    products_filepath = os.environ["PRODUCTS_YAML_FILE"]
    logger.info(f"Products yaml file: {products_filepath}")
    products = get_products_from_file(products_filepath)
    logger.info(products)
    create_tables()
    insert_products(products)
    list_all_products()
    list_all_schedule()
    # poll forever
    Poller().poll()

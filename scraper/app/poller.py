import logging
import os
import time
from datetime import timedelta, datetime

from selenium.common import TimeoutException

from app.db import list_all_schedule, Schedule, ScheduleStatus, Product
from app.scheduler import get_next_to_scrape, get_sleep_seconds
from app.scraper import get_product_price
from app.sns import publish_to_sns

logger = logging.getLogger(__name__)

MIN_SLEEP_SECONDS_BETWEEN_SCRAPES = int(os.getenv('SECONDS_BETWEEN_SCRAPES', 15))
logger.info(f'SECONDS_BETWEEN_SCRAPES={MIN_SLEEP_SECONDS_BETWEEN_SCRAPES}')


class Poller:

    def __init__(self, sns_topic_arn: str = None, scraping_period: timedelta = timedelta(days=1)):
        self.scraping_period = scraping_period
        self.sns_topic_arn = sns_topic_arn

    def poll(self):
        while True:
            logger.info("Polling...")
            list_all_schedule()
            next_to_run = get_next_to_scrape()
            if next_to_run and next_to_run.scheduled_for <= datetime.now():
                logger.info(f"Scraping for: schedule={next_to_run}")
                self.scrape_product(scheduled_job=next_to_run)
            self.sleep()

    def scrape_product(self, scheduled_job: Schedule):
        product = scheduled_job.product
        try:
            product_dto = get_product_price(id_=product.name, url=product.url, category=product.category)

            publish_to_sns(product_dto.to_json(), topic_arn=self.sns_topic_arn)

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

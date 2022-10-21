import logging
import os.path

from app.db import create_tables, list_all_products, list_all_schedule
from app.parser import extract_products_from_file
from app.poller import Poller
from app.product import update_products

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')
logger.info(f"SNS_TOPIC_ARN={TOPIC_ARN}")

if __name__ == '__main__':
    products_filepath = os.environ["PRODUCTS_YAML_FILE"]
    logger.info(f"Products yaml file: {products_filepath}")
    products = extract_products_from_file(products_filepath)
    logger.info(products)
    create_tables()
    update_products(products)
    list_all_products()
    list_all_schedule()

    # poll forever
    Poller(sns_topic_arn=TOPIC_ARN).poll()

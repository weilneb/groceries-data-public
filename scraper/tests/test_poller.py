import json
from unittest.mock import patch

import pytest

from app.db import Schedule, Product, get_all_schedules, ScheduleStatus
from app.product_dto import ProductDTO
from app.poller import Poller

MOCK_TOPIC_ARN = 'arn:aws:sns:ap-southeast-2:123:topic'
PRODUCT_URL = 'http://shop.com/a'


@pytest.mark.usefixtures("test_db")
class TestPoller:

    @patch('app.poller.get_product_price')
    @patch('app.poller.publish_to_sns')
    def test_parser(self, mock_publish_to_sns, mock_get_product_price):
        poller = Poller(sns_topic_arn=MOCK_TOPIC_ARN)
        product = Product(name='a', url=PRODUCT_URL, category='milk')
        schedule = Schedule(product=product)
        mock_get_product_price.return_value = ProductDTO(
            id='a',
            name='Milk 1L',
            category='milk',
            url=PRODUCT_URL,
            price=1.23,
        )
        poller.scrape_product(scheduled_job=schedule)
        mock_publish_to_sns.assert_called_once()

        json_dict = json.loads(mock_publish_to_sns.call_args.args[0])
        # TODO: mock time now, so we can assert on expected timestamp
        assert json_dict['url'] == PRODUCT_URL
        assert json_dict['id'] == 'a'
        assert json_dict['name'] == 'Milk 1L'
        assert json_dict['category'] == 'milk'

        arn_passed = mock_publish_to_sns.call_args.kwargs['topic_arn']
        assert arn_passed == MOCK_TOPIC_ARN

        schedules = get_all_schedules()

        # 1 for job just completed. 1 for the newly scheduled job.
        assert set(map(lambda x: x.status, schedules)) == {ScheduleStatus.SUCCESS, ScheduleStatus.SCHEDULED}

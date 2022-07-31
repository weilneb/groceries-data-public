import boto3
from botocore.config import Config

import os
import logging

logger = logging.getLogger(__name__)

TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
logger.info(f"SNS_TOPIC_ARN={TOPIC_ARN}")
DISABLE_PUBLISH = os.getenv('SNS_DISABLE_PUBLISH').lower() == 'true'


def publish_to_sns(payload_json: str, topic_arn=TOPIC_ARN):
    if not DISABLE_PUBLISH:
        client = boto3.client('sns', config=Config(region_name='ap-southeast-2'))
        response = client.publish(
            TopicArn=topic_arn,
            Message=payload_json,
        )
        logger.info(response)
    else:
        logger.warning('SNS publishing is disabled.')

import logging

import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)


def publish_to_sns(payload_json: str, topic_arn: str):
    if topic_arn:
        client = boto3.client('sns', config=Config(region_name='ap-southeast-2'))
        logger.info(f'Publishing JSON to SNS topic: {payload_json}')
        response = client.publish(
            TopicArn=topic_arn,
            Message=payload_json,
        )
        logger.info(response)
    else:
        logger.warning('Given SNS topic arn is blank, not publishing...')

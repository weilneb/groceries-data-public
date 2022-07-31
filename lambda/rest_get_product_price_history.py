import decimal
import json

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
groceries_data = dynamodb.Table('groceries_data')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def get_url_param(event):
    return event["queryStringParameters"]['url']


HEADERS = {'headers': {
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,GET'
}}


def lambda_handler(event, context):
    print(event)
    try:
        product_url = get_url_param(event)
    except KeyError:
        return {
            **HEADERS,
            'statusCode': 400,
            'body': json.dumps({'error': 'url query string param must be provided & be non-blank.'})
        }

    data = groceries_data.query(
        KeyConditionExpression=Key('url').eq(product_url)
    )
    items = data['Items']
    print(items)
    return {
        **HEADERS,
        'statusCode': 200,
        'body': json.dumps(items, cls=DecimalEncoder)
    }

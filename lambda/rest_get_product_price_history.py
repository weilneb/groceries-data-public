import json

import decimal
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
groceries_data = dynamodb.Table('gd_v2_price_history')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def get_id_param(event):
    product_id = event["queryStringParameters"]['id']
    if not product_id:
        raise ValueError("id must not be blank")
    return product_id


HEADERS = {'headers': {
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,GET'
}}


def lambda_handler(event, context):
    print(event)
    try:
        product_id = get_id_param(event)
    except Exception as err:
        return {
            **HEADERS,
            'statusCode': 400,
            'body': json.dumps({'error': 'id query string param must be provided & be non-blank.'})
        }

    data = groceries_data.query(
        KeyConditionExpression=Key('product_id').eq(product_id)
    )
    items = data['Items']
    print(items)
    return {
        **HEADERS,
        'statusCode': 200,
        'body': json.dumps(items, cls=DecimalEncoder)
    }

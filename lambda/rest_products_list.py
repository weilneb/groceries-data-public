import json
from collections import defaultdict

import boto3

dynamodb = boto3.resource('dynamodb')
products = dynamodb.Table('gd_v2_products')


def lambda_handler(event, context):
    response = products.scan()
    items = response['Items']
    print(items)

    category_to_prod = defaultdict(list)
    for item in items:
        category_to_prod[item['category']].append(item)

    print(category_to_prod)

    return {
        'statusCode': 200,
        'body': json.dumps(category_to_prod),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        }
    }

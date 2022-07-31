import json
import boto3
from collections import defaultdict

dynamodb = boto3.resource('dynamodb')
groceries_categories = dynamodb.Table('groceries_categories')


def lambda_handler(event, context):
    response = groceries_categories.scan()
    items = response['Items']
    categories = set(map(lambda x: x['category'], items))

    d = defaultdict(list)
    for item in items:
        d[item['category']].append(item['url'])
    as_list = []
    for k, v in d.items():
        as_list.append({
            'category': k,
            'urls': v
        })
    return {
        'statusCode': 200,
        'body': json.dumps(as_list),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        }
    }

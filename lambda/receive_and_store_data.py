import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
groceries_data = dynamodb.Table('groceries_data')
groceries_categories = dynamodb.Table('groceries_categories')


def lambda_handler(event, context):
    print("Event:", event)
    msg = event['Records'][0]['Sns']['Message']
    print("Message:", msg)
    j = json.loads(msg, parse_float=Decimal)
    groceries_data.put_item(Item=j)

    category_dict = {
        'category': j['category'],
        'url': j['url']
    }
    result = groceries_categories.get_item(Key=category_dict)
    print('Category item:', result)
    if 'Item' not in result:
        groceries_categories.put_item(Item=category_dict)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully stored product price data.')
    }

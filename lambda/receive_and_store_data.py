import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
price_history = dynamodb.Table('gd_v2_price_history')
products = dynamodb.Table('gd_v2_products')


def lambda_handler(event, context):
    print("Event:", event)
    msg = event['Records'][0]['Sns']['Message']
    print("Message:", msg)
    j = json.loads(msg, parse_float=Decimal)
    print("Payload:", j)

    product = {k: j[k] for k in ('id', 'name', 'url', 'category')}
    print("Product:", product)

    product_id = product['id']
    assert product_id

    products.put_item(Item=product)

    price_row = {"product_id": product_id,
                 "timestamp": j["timestamp"],
                 "price": j["price"]
                 }
    assert price_row["price"]
    assert price_row["timestamp"]

    print("Price row:", price_row)
    price_history.put_item(Item=price_row)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully stored product price data.')
    }

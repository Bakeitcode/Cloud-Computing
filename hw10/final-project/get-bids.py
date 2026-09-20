import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("bids")


def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(x) for x in obj]
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


def lambda_handler(event, context):
    print("Event:", event)

    auction_id = event.get("auctionId")

    response = table.query(
        KeyConditionExpression=Key("auctionId").eq(auction_id),
        ScanIndexForward=False
    )

    items = response.get("Items", [])
    items = convert_decimal(items)

    print("DynamoDB response:", response)
    print("Items:", items)

    return {
        "bids": items
    }
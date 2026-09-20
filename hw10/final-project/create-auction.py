import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('auctions')

def lambda_handler(event, context):
    print("Event: ", event)

    auction_id = str(uuid.uuid4())

    item = {
        "auctionId": auction_id,
        "itemName": event.get("itemName"),
        "description": event.get("description"),
        "reserve": event.get("reserve"),
        "auctionStatus": "OPEN",
        "winningUserId": None
    }

    table.put_item(Item=item)

    return {
        "success": True,
        "auction": item
    }

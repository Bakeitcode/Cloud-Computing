import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("auctions")
print("GHA Deploy test3 - HW10")


def lambda_handler(event, context):
    print("Event: ", event)

    auction_id = event.get("auctionId")

    if auction_id:
        response = table.get_item(
            Key={
                "auctionId": auction_id
            }
        )
        item = response.get("Item")

        return {
            "success": True,
            "auction": item
        }

    response = table.scan()
    items = response.get("Items", [])

    return {
        "success": True,
        "auctions": items
    }

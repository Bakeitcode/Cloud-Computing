import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
ddb_client = boto3.client("dynamodb")

auctions_table = dynamodb.Table("auctions")
bids_table = dynamodb.Table("bids")
users_table = dynamodb.Table("users")


def decimal_to_native(value):
    if isinstance(value, list):
        return [decimal_to_native(v) for v in value]
    if isinstance(value, dict):
        return {k: decimal_to_native(v) for k, v in value.items()}
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    return value


def lambda_handler(event, context):
    print("Event:", event)

    auction_id = event.get("auctionId")
    if not auction_id:
        return {"closed": False, "message": "auctionId is required"}

    # 1. Load auction
    auction_resp = auctions_table.get_item(Key={"auctionId": auction_id})
    auction = auction_resp.get("Item")
    if not auction:
        return {"closed": False, "message": "Auction does not exist"}

    # 2. Must be OPEN
    if auction.get("auctionStatus") != "OPEN":
        return {"closed": False, "message": "Auction is not open"}

    # 3. Load highest bid
    bids_resp = bids_table.query(
        KeyConditionExpression=Key("auctionId").eq(auction_id),
        ScanIndexForward=False,
        Limit=1
    )
    highest_bid_item = bids_resp.get("Items", [])
    if not highest_bid_item:
        return {"closed": False, "message": "Auction has no bids"}

    highest_bid = highest_bid_item[0]
    winning_bid_amt = highest_bid["bidAmt"]
    winning_user_id = highest_bid["userId"]

    # 4. Reserve must be met
    reserve = auction.get("reserve", Decimal("0"))
    if winning_bid_amt < reserve:
        return {"closed": False, "message": "Reserve not met"}

    # 5. Winner must exist
    user_resp = users_table.get_item(Key={"userId": winning_user_id})
    winner = user_resp.get("Item")
    if not winner:
        return {"closed": False, "message": "Winning user does not exist"}

    # 6. Optional safety: ensure enough balance at close time
    current_balance = winner.get("acctBalance", Decimal("0"))
    if current_balance < winning_bid_amt:
        return {"closed": False, "message": "Winning user no longer has sufficient funds"}

    # 7. Transaction: close auction + debit winner
    ddb_client.transact_write_items(
        TransactItems=[
            {
                "Update": {
                    "TableName": "auctions",
                    "Key": {
                        "auctionId": {"S": auction_id}
                    },
                    "UpdateExpression": "SET auctionStatus = :closed, winningUserId = :winner",
                    "ConditionExpression": "auctionStatus = :open",
                    "ExpressionAttributeValues": {
                        ":closed": {"S": "CLOSED"},
                        ":winner": {"S": winning_user_id},
                        ":open": {"S": "OPEN"}
                    }
                }
            },
            {
                "Update": {
                    "TableName": "users",
                    "Key": {
                        "userId": {"S": winning_user_id}
                    },
                    "UpdateExpression": "SET acctBalance = acctBalance - :bidAmt",
                    "ConditionExpression": "acctBalance >= :bidAmt",
                    "ExpressionAttributeValues": {
                        ":bidAmt": {"N": str(winning_bid_amt)}
                    }
                }
            }
        ]
    )

    return {
        "closed": True,
        "auctionId": auction_id,
        "winningUserId": winning_user_id,
        "bidAmt": decimal_to_native(winning_bid_amt),
        "itemName": auction.get("itemName")
    }
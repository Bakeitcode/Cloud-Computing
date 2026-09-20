import json


def lambda_handler(event, context):
    print("Event:", event)

    for record in event.get("Records", []):
        body = record.get("body", "")

        # SQS message from SNS subscription
        if body:
            try:
                envelope = json.loads(body)

                # Case 1: SNS -> SQS for new highest bidder
                if isinstance(envelope, dict) and "Message" in envelope:
                    print(envelope["Message"])
                    continue

                # Case 2: direct JSON body from some other source
                if isinstance(envelope, dict):
                    event_type = envelope.get("eventType")

                    if event_type == "AUCTION_CLOSED":
                        auction_id = envelope.get("auctionId", "")
                        user_id = envelope.get("userId", "")
                        item_name = envelope.get("itemName", "")
                        bid_amt = envelope.get("bidAmt", "")
                        print(
                            f"Auction {auction_id} is now closed. "
                            f"User {user_id} wins {item_name} with a bid of {bid_amt}"
                        )
                        continue

                    if event_type == "NEW_HIGHEST_BIDDER":
                        user_id = envelope.get("userId", "")
                        bid_amt = envelope.get("bidAmt", "")
                        print(f"New highest bidder: user {user_id} bid {bid_amt}")
                        continue
            except json.JSONDecodeError:
                pass

        # EventBridge Pipe / DynamoDB stream style event
        if record.get("eventName") == "MODIFY":
            new_image = record.get("dynamodb", {}).get("NewImage", {})
            old_image = record.get("dynamodb", {}).get("OldImage", {})

            new_status = new_image.get("auctionStatus", {}).get("S")
            old_status = old_image.get("auctionStatus", {}).get("S")

            if new_status == "CLOSED" and old_status != "CLOSED":
                auction_id = new_image.get("auctionId", {}).get("S", "")
                user_id = new_image.get("winningUserId", {}).get("S", "")
                item_name = new_image.get("itemName", {}).get("S", "")

                # bidAmt is not in the auctions table, so look for it if your pipe/input
                # transformation included it; otherwise this will print blank.
                bid_amt = (
                    new_image.get("bidAmt", {}).get("N")
                    or new_image.get("bidAmt", {}).get("S")
                    or ""
                )

                print(
                    f"Auction {auction_id} is now closed. "
                    f"User {user_id} wins {item_name} with a bid of {bid_amt}"
                )

    return {
        "logged": True
    }
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def lambda_handler(event, context):
    print("Event:", event)

    user_id = str(uuid.uuid4())

    item = {
        "userId": user_id,
        "name": event.get("name"),
        "acctBalance": event.get("acctBalance")
    }

    table.put_item(Item=item)

    return {
        "success": True,
        "user": item
    }
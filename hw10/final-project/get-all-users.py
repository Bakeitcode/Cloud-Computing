import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')
print("GHA deploy test2 - hw10")
def lambda_handler(event, context):
    print("Event:", event)

    response = table.scan()
    items = response.get("Items", [])

    return {
        "success": True,
        "users": items
    }
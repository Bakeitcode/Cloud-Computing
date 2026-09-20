import json
import os
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        body = event.get("body", "{}")

        if isinstance(body, str):
            body = json.loads(body, parse_float=Decimal, parse_int=Decimal)

        name = body.get("name")
        age = body.get("age")
        profession = body.get("profession")

        if name is None or age is None or profession is None:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Request must include name, age, and profession"
                })
            }

        item = {
            "name": name,
            "age": age,
            "profession": profession
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Item written to DynamoDB",
                "item": {
                    "name": name,
                    "age": int(age) if isinstance(age, Decimal) else age,
                    "profession": profession
                }
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error writing to DynamoDB",
                "error": str(e)
            })
        }
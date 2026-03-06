import json
import boto3

s3 = boto3.client('s3')

def put_object_handler(event, context):

    bucket = event["pathParameters"]["bucket-name"]
    obj = event["pathParameters"]["object-name"]

    body = event["body"]

    s3.put_object(
        Bucket=bucket,
        Key=obj,
        Body=body
    )

    data = {
        "message": f"Object {obj} uploaded to {bucket}"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
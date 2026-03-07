import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def put_object_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    bucket_name = event["pathParameters"]["bucket-name"]
    object_name = event["pathParameters"]["object-name"]
    body = event["body"]

    logger.info("bucket-name: %s", bucket_name)
    logger.info("object-name: %s", object_name)
    logger.info("request body: %s", body)

    s3.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=body
    )

    data = {
        "message": f"Object {object_name} uploaded to {bucket_name}"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
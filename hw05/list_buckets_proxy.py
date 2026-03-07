import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def list_buckets_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    response = s3.list_buckets()
    buckets = [b["Name"] for b in response["Buckets"]]

    logger.info("Buckets found: %s", buckets)

    data = {
        "count": len(buckets),
        "buckets": buckets
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
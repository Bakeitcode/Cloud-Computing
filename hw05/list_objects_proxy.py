import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def list_objects_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    bucket_name = event["pathParameters"]["bucket-name"]
    logger.info("bucket-name: %s", bucket_name)

    response = s3.list_objects_v2(Bucket=bucket_name)

    objects = []
    if "Contents" in response:
        objects = [obj["Key"] for obj in response["Contents"]]

    logger.info("Objects found in %s: %s", bucket_name, objects)

    data = {
        "count": len(objects),
        "objects": objects
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def del_object_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    bucket_name = event["pathParameters"]["bucket-name"]
    object_name = event["pathParameters"]["object-name"]

    logger.info("bucket-name: %s", bucket_name)
    logger.info("object-name: %s", object_name)

    s3.delete_object(
        Bucket=bucket_name,
        Key=object_name
    )

    data = {
        "message": f"Deleted object {object_name} from bucket {bucket_name}"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
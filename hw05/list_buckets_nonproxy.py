import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")


def list_buckets_nonproxy_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response.get("Buckets", [])]

    logger.info("Buckets found: %s", buckets)

    return buckets
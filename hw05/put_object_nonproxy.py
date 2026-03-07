import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")


def put_object_nonproxy_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    bucket_name = event.get("bucket-name")
    object_name = event.get("object-name")
    body = event.get("body")

    logger.info("bucket-name: %s", bucket_name)
    logger.info("object-name: %s", object_name)
    logger.info("request body: %s", body)

    # FIX: API Gateway non-proxy mapping may pass the request body as a parsed JSON object (dict)
    # instead of a string. s3.put_object() requires the Body parameter to be a string or bytes,
    # so convert the body to JSON text if it is not already a string.
    if not isinstance(body, str):
        body = json.dumps(body)

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=body
        )
        return f"Successfully uploaded object {object_name} to bucket {bucket_name}"
    except Exception as e:
        logger.exception("Error uploading object")
        return f"Error uploading object {object_name} to bucket {bucket_name}: {str(e)}"
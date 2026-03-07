import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")


def del_object_nonproxy_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    bucket_name = event.get("bucket-name")
    object_name = event.get("object-name")

    logger.info("bucket-name: %s", bucket_name)
    logger.info("object-name: %s", object_name)

    try:
        s3.delete_object(
            Bucket=bucket_name,
            Key=object_name
        )
        return f"Successfully deleted object {object_name} from bucket {bucket_name}"
    except Exception as e:
        logger.exception("Error deleting object")
        return f"Error deleting object {object_name} from bucket {bucket_name}: {str(e)}"
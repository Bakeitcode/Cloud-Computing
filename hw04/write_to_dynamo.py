import os
import json
import logging
import urllib.parse
from datetime import datetime, timezone

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")


def write_metadata(event, context):
    """
    Trigger: S3 "All object create events"
    Action: Read object metadata and write a record to DynamoDB
    DynamoDB keys (recommended):
      - PK: bucket_arn (String)
      - SK: upload_datetime (String)
    Required attributes to store (exact names):
      - file_name, file_size, upload_datetime, bucket_arn, etag
    """
    table_name = os.environ.get("TABLE_NAME")
    if not table_name:
        raise RuntimeError("Missing required env var TABLE_NAME")

    table = dynamodb.Table(table_name)

    logger.info("Received event: %s", json.dumps(event))

    # S3 can batch multiple records; handle them all
    results = []
    for record in event.get("Records", []):
        if record.get("eventSource") != "aws:s3":
            logger.warning("Skipping non-s3 record: %s", record.get("eventSource"))
            continue

        bucket_name = record["s3"]["bucket"]["name"]
        raw_key = record["s3"]["object"]["key"]
        # Keys in events are URL-encoded
        object_key = urllib.parse.unquote_plus(raw_key)

        # Pull basic size if present in event; still confirm via HEAD for etag, etc.
        size_from_event = record["s3"]["object"].get("size")

        # HeadObject gives us authoritative metadata (ETag, ContentLength, etc.)
        head = s3.head_object(Bucket=bucket_name, Key=object_key)

        file_size = int(head.get("ContentLength", size_from_event or 0))
        # ETag often comes with quotes in HeadObject response
        etag = head.get("ETag", "").strip('"')

        # Build the bucket ARN
        bucket_arn = f"arn:aws:s3:::{bucket_name}"

        # Use an ISO-8601 UTC timestamp for sortable string SK
        upload_datetime = datetime.now(timezone.utc).isoformat()

        item = {
            "bucket_arn": bucket_arn,
            "upload_datetime": upload_datetime,
            "file_name": object_key,
            "file_size": file_size,
            "etag": etag,
        }

        # Log exactly what we are writing (minimum requirement)
        logger.info("Writing item to DynamoDB: %s", json.dumps(item))

        table.put_item(Item=item)
        results.append(item)

    return {
        "statusCode": 200,
        "body": json.dumps({"written": results}),
    }
import os
import json
import logging
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")


def _decimal_to_native(obj):
    """
    DynamoDB can return Decimal for numbers.
    Convert Decimal -> int/float so json.dumps works.
    """
    if isinstance(obj, list):
        return [_decimal_to_native(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _decimal_to_native(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        # Convert to int if it's integral, else float
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


def _response(status_code: int, payload: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json"
        },
        "body": json.dumps(_decimal_to_native(payload)),
    }


def read_metadata(event, context):
    """
    Lambda Function URL handler.

    - If query string contains ?name=<filename>, returns only items whose file_name matches.
    - If no query string, returns all items (Scan).

    Uses env var TABLE_NAME for DynamoDB table name (no hardcoding).
    Returns JSON:
      { "items": [ {bucket_arn, etag, file_name, upload_datetime, file_size}, ... ] }
    """
    table_name = os.environ.get("TABLE_NAME")
    if not table_name:
        logger.error("Missing required env var TABLE_NAME")
        return _response(500, {"error": "Server misconfigured: missing TABLE_NAME"})

    table = dynamodb.Table(table_name)

    logger.info("Incoming event: %s", json.dumps(event))

    # For Function URLs, query params appear here
    params = event.get("queryStringParameters") or {}
    name = params.get("name") if isinstance(params, dict) else None

    try:
        if name:
            # NOTE: True DynamoDB Query requires key attributes or a GSI.
            # Since the table key is (bucket_arn, upload_datetime), we use Scan + FilterExpression.
            logger.info("Filtering by file_name (name param): %s", name)

            resp = table.scan(
                FilterExpression=Attr("file_name").eq(name)
            )
            items = resp.get("Items", [])

            # Handle pagination (Scan can return LastEvaluatedKey)
            while "LastEvaluatedKey" in resp:
                resp = table.scan(
                    FilterExpression=Attr("file_name").eq(name),
                    ExclusiveStartKey=resp["LastEvaluatedKey"]
                )
                items.extend(resp.get("Items", []))
        else:
            logger.info("No name param provided; scanning for all items")
            resp = table.scan()
            items = resp.get("Items", [])

            while "LastEvaluatedKey" in resp:
                resp = table.scan(ExclusiveStartKey=resp["LastEvaluatedKey"])
                items.extend(resp.get("Items", []))

        # Ensure the response includes the expected fields (and only those if you want)
        cleaned = []
        for it in items:
            cleaned.append({
                "bucket_arn": it.get("bucket_arn", ""),
                "etag": it.get("etag", ""),
                "file_name": it.get("file_name", ""),
                "upload_datetime": it.get("upload_datetime", ""),
                "file_size": it.get("file_size", ""),
            })

        return _response(200, {"items": cleaned})

    except Exception as e:
        logger.exception("Error reading DynamoDB: %s", str(e))
        return _response(500, {"error": "Failed to read from DynamoDB"})
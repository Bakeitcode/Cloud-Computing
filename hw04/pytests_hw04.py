import os
import time
import uuid
import json
import datetime

import boto3
import pytest
import requests
from boto3.dynamodb.conditions import Attr


REGION = os.getenv("AWS_REGION", "us-east-1")
BUCKET = os.getenv("HW04_BUCKET_NAME")
TABLE_NAME = os.getenv("HW04_TABLE_NAME")
FUNCTION_URL = (os.getenv("HW04_FUNCTION_URL") or "").strip()


def _require_env():
    missing = []
    if not BUCKET:
        missing.append("HW04_BUCKET_NAME")
    if not TABLE_NAME:
        missing.append("HW04_TABLE_NAME")
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")


def _poll_for_item(table, file_name: str, timeout_s: int = 90, poll_s: float = 2.0):
    """
    Poll DynamoDB until an item appears with file_name == <file_name>.
    Uses Scan + FilterExpression because the table keys are (bucket_arn, upload_datetime).
    """
    deadline = time.time() + timeout_s

    while time.time() < deadline:
        resp = table.scan(FilterExpression=Attr("file_name").eq(file_name))
        items = resp.get("Items", [])
        if items:
            return items
        time.sleep(poll_s)

    raise AssertionError(f"Timed out waiting for DynamoDB item for file_name={file_name}")


@pytest.mark.integration
def test_s3_upload_triggers_lambda_and_writes_dynamo():
    _require_env()

    s3 = boto3.client("s3", region_name=REGION)
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    table = dynamodb.Table(TABLE_NAME)

    # Unique object key each run
    key = f"gha-test-{uuid.uuid4().hex}.txt"
    body = f"hello from gha {uuid.uuid4().hex}".encode("utf-8")

    # 1) Upload to S3 (should trigger hw04-write-to-dynamo)
    s3.put_object(Bucket=BUCKET, Key=key, Body=body)

    # 2) Assert object exists in S3
    head = s3.head_object(Bucket=BUCKET, Key=key)
    assert head["ContentLength"] == len(body)

    s3_etag = head.get("ETag", "").strip('"')
    assert s3_etag, "S3 ETag was empty"

    # 3) Poll DynamoDB until writer lambda writes the record
    items = _poll_for_item(table, file_name=key, timeout_s=120, poll_s=2.0)

    # If multiple matches (rare, but possible), pick the newest upload_datetime
    def _dt(it):
        return it.get("upload_datetime", "")

    item = sorted(items, key=_dt, reverse=True)[0]

    # 4) Assert required fields exist
    for field in ["bucket_arn", "upload_datetime", "file_name", "file_size", "etag"]:
        assert field in item, f"Missing field '{field}' in DynamoDB item: {item}"

    # 5) Assert values match expectations
    assert item["file_name"] == key
    assert str(item["bucket_arn"]).endswith(BUCKET)  # arn:aws:s3:::<bucket>
    assert int(item["file_size"]) == len(body)
    assert str(item["etag"]) == s3_etag
    assert isinstance(item["upload_datetime"], str) and len(item["upload_datetime"]) > 0

    # 6) Optional: verify read-lambda Function URL returns the item
    if FUNCTION_URL:
        resp = requests.get(FUNCTION_URL, params={"name": key}, timeout=20)
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert any(x.get("file_name") == key for x in data["items"]), (
            "Function URL did not return the uploaded object. "
            f"Got: {json.dumps(data)[:800]}"
        )
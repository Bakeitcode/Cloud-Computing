import os
import uuid
import pytest

import main_client_api as client_app


CLIENT_BUCKET = os.environ["HW03_CLIENT_BUCKET"]


def _unique_key():
    return f"test-{uuid.uuid4().hex}.txt"


def test_list_buckets_is_denied_but_handled(capsys):
    # Learner Lab often denies s3:ListAllMyBuckets explicitly.
    client_app.list_buckets()
    out = capsys.readouterr().out
    assert "Error listing buckets" in out


def test_upload_list_get_delete_roundtrip(tmp_path):
    key = _unique_key()
    local_file = tmp_path / "hello.txt"
    local_file.write_text("hello from pytest", encoding="utf-8")

    # Upload (tests your TODO #9 upload_file_to_bucket implementation)
    client_app.upload_file_to_bucket(str(local_file), CLIENT_BUCKET, key)

    # List (tests your TODO #2 list_objects_v2 implementation)
    objs = client_app.list_contents(CLIENT_BUCKET, "")
    assert key in objs

    # Get (tests your TODO #3 get_object implementation)
    data = client_app.get_file(CLIENT_BUCKET, "", key)
    assert data is not None
    assert data.decode("utf-8") == "hello from pytest"

    # Delete (your delete_object() is interactive, so delete via boto3 client directly)
    client_app.s3_client.delete_object(Bucket=CLIENT_BUCKET, Key=key)

    # Confirm deletion
    objs_after = client_app.list_contents(CLIENT_BUCKET, "")
    assert key not in objs_after

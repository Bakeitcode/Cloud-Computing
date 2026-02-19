import os
import uuid
import pytest

import main_resource_api as res_app


RESOURCE_BUCKET = os.environ["HW03_RESOURCE_BUCKET"]


def _unique_key():
    return f"test-{uuid.uuid4().hex}.txt"


def test_upload_list_get_delete_roundtrip(tmp_path):
    key = _unique_key()
    local_file = tmp_path / "hello.txt"
    local_file.write_text("hello from resource pytest", encoding="utf-8")

    # Upload using resource API (Bucket.upload_file)
    bucket = res_app.s3_resource.Bucket(RESOURCE_BUCKET)
    bucket.upload_file(str(local_file), key)

    # List using your list_contents (Bucket.objects.filter)
    objs = res_app.list_contents(RESOURCE_BUCKET, "")
    assert key in objs

    # Get using your get_file (Object + obj.get())
    data = res_app.get_file(RESOURCE_BUCKET, "", key)
    assert data is not None
    assert data.decode("utf-8") == "hello from resource pytest"

    # Delete using resource Object.delete()
    obj = res_app.s3_resource.Object(RESOURCE_BUCKET, key)
    obj.delete()

    objs_after = res_app.list_contents(RESOURCE_BUCKET, "")
    assert key not in objs_after

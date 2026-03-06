import json
import boto3

s3 = boto3.client("s3")


def list_objects_handler(event, context):
    path_params = event.get("pathParameters") or {}
    bucket_name = path_params.get("bucket-name")

    if not bucket_name:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Missing required path parameter: bucket-name"
            })
        }

    response = s3.list_objects_v2(Bucket=bucket_name)
    contents = response.get("Contents", [])
    object_names = [obj["Key"] for obj in contents]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "count": len(object_names),
            "objects": object_names
        })
    }
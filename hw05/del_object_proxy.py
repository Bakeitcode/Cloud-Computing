import json
import boto3

s3 = boto3.client("s3")


def del_object_handler(event, context):
    path_params = event.get("pathParameters") or {}
    bucket_name = path_params.get("bucket-name")
    object_name = path_params.get("object-name")

    if not bucket_name or not object_name:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Missing required path parameters: bucket-name and/or object-name"
            })
        }

    s3.delete_object(Bucket=bucket_name, Key=object_name)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": f"Deleted object {object_name} from bucket {bucket_name}"
        })
    }
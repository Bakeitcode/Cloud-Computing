import json
import boto3

s3 = boto3.client("s3")


def list_buckets_handler(event, context):
    response = s3.list_buckets()
    bucket_names = [bucket["Name"] for bucket in response.get("Buckets", [])]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "count": len(bucket_names),
            "buckets": bucket_names
        })
    }
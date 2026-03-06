import json
import boto3

s3 = boto3.client('s3')

def list_objects_handler(event, context):

    bucket_name = event["pathParameters"]["bucket-name"]

    response = s3.list_objects_v2(Bucket=bucket_name)

    objects = []
    if "Contents" in response:
        objects = [obj["Key"] for obj in response["Contents"]]

    data = {
        "count": len(objects),
        "objects": objects
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
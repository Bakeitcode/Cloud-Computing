import json
import boto3

s3 = boto3.client('s3')

def list_buckets_handler(event, context):

    response = s3.list_buckets()
    buckets = [b['Name'] for b in response['Buckets']]

    data = {
        "count": len(buckets),
        "buckets": buckets
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
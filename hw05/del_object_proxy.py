import json
import boto3

s3 = boto3.client('s3')

def del_object_handler(event, context):

    bucket = event["pathParameters"]["bucket-name"]
    obj = event["pathParameters"]["object-name"]

    s3.delete_object(
        Bucket=bucket,
        Key=obj
    )

    data = {
        "message": f"Deleted object {obj} from bucket {bucket}"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
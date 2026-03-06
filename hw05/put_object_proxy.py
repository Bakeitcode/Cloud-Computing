import json
import boto3

s3 = boto3.client("s3")


def put_object_handler(event, context):
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

    body = event.get("body")
    if body is None:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Missing request body"
            })
        }

    # If API Gateway sends the body as a string, validate that it is JSON.
    try:
        parsed_json = json.loads(body)
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Request body must be valid JSON"
            })
        }

    s3.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=json.dumps(parsed_json),
        ContentType="application/json"
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": f"Object {object_name} uploaded to {bucket_name}"
        })
    }
from flask import Flask, render_template, request, redirect, url_for, abort
import boto3
from botocore.exceptions import ClientError
import hashlib
import logging
import os

app = Flask(__name__)

# Logging to console; same code will work locally, in Docker, and in ECS/CloudWatch
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TABLE_NAME = os.getenv("TABLE_NAME", "hw06-urls")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)


def generate_short_key(long_url: str) -> str:
    return hashlib.md5(long_url.encode("utf-8")).hexdigest()[:7]


def get_all_urls():
    try:
        response = table.scan()
        items = response.get("Items", [])
        items.sort(key=lambda x: x.get("key", ""))
        return items
    except ClientError as e:
        logger.error("Error scanning DynamoDB table: %s", e)
        return []


@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    error = None

    if request.method == "POST":
        long_url = request.form.get("long_url", "").strip()

        if not long_url:
            error = "Please enter a URL."
        elif not (long_url.startswith("http://") or long_url.startswith("https://")):
            error = "Please include http:// or https:// in the URL."
        else:
            key = generate_short_key(long_url)

            logger.info("Generate pressed. long_url=%s key=%s", long_url, key)

            try:
                existing = table.get_item(Key={"key": key})
                existing_item = existing.get("Item")

                if existing_item and existing_item.get("long_url") != long_url:
                    error = (
                        f"Hash collision detected for key '{key}'. "
                        "Try a different URL."
                    )
                else:
                    table.put_item(
                        Item={
                            "key": key,
                            "long_url": long_url
                        }
                    )
                    short_url = url_for("redirect_short_url", key=key, _external=True)

            except ClientError as e:
                logger.error("Error writing to DynamoDB: %s", e)
                error = "Failed to store URL in DynamoDB."

    items = get_all_urls()
    return render_template("index.html", short_url=short_url, error=error, items=items)


@app.route("/<key>", methods=["GET"])
def redirect_short_url(key):
    try:
        response = table.get_item(Key={"key": key})
        item = response.get("Item")

        if not item:
            abort(404)

        long_url = item["long_url"]
        return redirect(long_url, code=301)

    except ClientError as e:
        logger.error("Error looking up key in DynamoDB: %s", e)
        abort(500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
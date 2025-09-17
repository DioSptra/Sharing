import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import ClientError
from datetime import datetime
import traceback

app = Flask(__name__)

# Config dari ENV
S3_BUCKET = os.getenv("S3_BUCKET", "diobucket-1")
S3_REGION = os.getenv("S3_REGION", "ap-southeast-1")
S3_PREFIX = os.getenv("S3_PREFIX", "GUI/")  # default folder GUI/
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Client boto3 (pilih pakai creds env atau unsigned/public)
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    s3 = boto3.client(
        "s3",
        region_name=S3_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
else:
    s3 = boto3.client("s3", region_name=S3_REGION, config=Config(signature_version=UNSIGNED))

# helper build object url
def s3_url(key: str) -> str:
    return f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{key}"

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})

# Upload
@app.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "file required"}), 400

    f = request.files["file"]
    filename = secure_filename(f.filename)
    if filename == "":
        return jsonify({"error": "invalid filename"}), 400

    key = f"{S3_PREFIX}{filename}"  # selalu masuk ke folder GUI/

    try:
        s3.upload_fileobj(
            f,
            S3_BUCKET,
            key,
            ExtraArgs={"ContentType": f.content_type, "ACL": "public-read"}
        )
        return jsonify({"key": key, "url": s3_url(key)}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "upload failed", "message": str(e)}), 500

# List
@app.route("/api/images", methods=["GET"])
def list_images():
    try:
        resp = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_PREFIX, MaxKeys=1000)
        items = []
        for obj in resp.get("Contents", []):
            key = obj["Key"]
            if key.endswith("/"):  # skip folder marker
                continue
            items.append({
                "key": key,
                "url": s3_url(key),
                "size": obj.get("Size"),
                "last_modified": obj.get("LastModified").isoformat() if obj.get("LastModified") else None
            })
        return jsonify(items)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "list failed", "message": str(e)}), 500

# Delete
@app.route("/api/delete/<path:key>", methods=["DELETE", "POST"])
def delete_image(key):
    if not key.startswith(S3_PREFIX):
        key = f"{S3_PREFIX}{key}"
    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=key)
        return jsonify({"deleted": key})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "delete failed", "message": str(e)}), 500

# Update (replace existing file)
@app.route("/api/update/<path:key>", methods=["POST"])
def update_image(key):
    if "file" not in request.files:
        return jsonify({"error": "file required"}), 400

    f = request.files["file"]
    if not key.startswith(S3_PREFIX):
        key = f"{S3_PREFIX}{key}"

    try:
        s3.upload_fileobj(
            f,
            S3_BUCKET,
            key,
            ExtraArgs={"ContentType": f.content_type, "ACL": "public-read"}
        )
        return jsonify({"key": key, "url": s3_url(key)})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "update failed", "message": str(e)}), 500

# Favicon dummy
@app.route("/favicon.ico")
def favicon():
    return "", 204

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

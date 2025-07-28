import json
import base64
import time
import boto3
from botocore.exceptions import ClientError

DYNAMO_TABLE = "user-clicks"
AWS_REGION = "us-east-1"

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMO_TABLE)

def process_record(record):
    try:
        data = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        click = json.loads(data)
        
        item = {
            "user_id": str(click["user_id"]),
            "timestamp": int(click["timestamp"]),
            "product_id": str(click["product_id"]),
            "expiry_time": int(time.time()) + 86400  # 24hrs TTL
        }
        
        table.put_item(Item=item)
        return {"status": "success", "record": item}
        
    except Exception as e:
        return {"status": "error", "error": str(e)}

def lambda_handler(event, context):
    results = [process_record(r) for r in event.get("Records", [])]
    successes = sum(1 for r in results if r["status"] == "success")
    
    return {
        "processed": successes,
        "errors": len(results) - successes,
        "details": results
    }
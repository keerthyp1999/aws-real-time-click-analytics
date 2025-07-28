import json
import random
import time
import boto3

KINESIS_STREAM = "click-stream"
AWS_REGION = "us-east-1"

def generate_clicks():
    kinesis = boto3.client("kinesis", region_name=AWS_REGION)
    products = ["B08N5KWB9H", "B07PGL7N7J", "B08L5V988D"]
    
    try:
        while True:
            click = {
                "user_id": random.randint(1000, 9999),
                "product_id": random.choice(products),
                "timestamp": int(time.time())
            }
            kinesis.put_record(
                StreamName=KINESIS_STREAM,
                Data=json.dumps(click),
                PartitionKey=str(click["user_id"])
            )
            print(f"Sent: {click}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    generate_clicks()
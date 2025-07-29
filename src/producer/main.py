import json
import random
import time
import boto3
from concurrent.futures import ThreadPoolExecutor

class ClickGenerator:
    def __init__(self):
        self.kinesis = boto3.client("kinesis", region_name="us-east-1")
        self.products = self._load_product_catalog()
        
    def _load_product_catalog(self):
        """Mock product catalog from Amazon"""
        return [
            "B08N5KWB9H",  
            "B07PGL7N7J", 
            "B08L5V988D"   
        ]
    
    def _generate_click(self):
        return {
            "user_id": random.randint(1000, 9999),
            "session_id": f"session_{random.randint(1, 100)}",
            "product_id": random.choice(self.products),
            "action": random.choice(["view", "add_to_cart", "purchase"]),
            "timestamp": int(time.time()),
            "device": random.choice(["mobile", "desktop", "tablet"])
        }

    def send_to_kinesis(self, batch_size=10):
        """Optimized batch producer"""
        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                batch = [{
                    "Data": json.dumps(self._generate_click()),
                    "PartitionKey": str(random.randint(1, 10))
                } for _ in range(batch_size)]
                
                try:
                    response = self.kinesis.put_records(
                        Records=batch,
                        StreamName="click-stream"
                    )
                    print(f"Sent {len(batch)} records | Failed: {response['FailedRecordCount']}")
                    time.sleep(0.2)
                except Exception as e:
                    print(f"Producer error: {str(e)}")

if __name__ == "__main__":
    ClickGenerator().send_to_kinesis()
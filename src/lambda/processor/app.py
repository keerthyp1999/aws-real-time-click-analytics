import os
import json
import base64
import boto3
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ClickEvent:
    user_id: str
    product_id: str
    timestamp: int
    action: str
    device: str

class ClickProcessor:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(os.getenv("DYNAMO_TABLE"))
        self.sns = boto3.client("sns")
        
    def _parse_record(self, record: Dict) -> ClickEvent:
        data = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        return ClickEvent(**json.loads(data))
    
    def _store_click(self, event: ClickEvent) -> bool:
        try:
            self.table.put_item(
                Item={
                    "user_id": event.user_id,
                    "timestamp": event.timestamp,
                    "product_id": event.product_id,
                    "action": event.action,
                    "device": event.device,
                    "expiry_time": int(time.time()) + 86400  # 24h TTL
                },
                ConditionExpression="attribute_not_exists(user_id)"  # Deduplication
            )
            return True
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            print(f"Duplicate event: {event.user_id}-{event.timestamp}")
            return False
        except Exception as e:
            self.sns.publish(
                TopicArn=os.getenv("ALERT_TOPIC_ARN"),
                Message=f"Failed to process click: {str(e)}"
            )
            raise

    def process(self, event: Dict) -> Dict:
        results = {"success": 0, "duplicates": 0, "errors": 0}
        for record in event.get("Records", []):
            try:
                click = self._parse_record(record)
                if self._store_click(click):
                    results["success"] += 1
                else:
                    results["duplicates"] += 1
            except Exception:
                results["errors"] += 1
        return results

def lambda_handler(event, context):
    return ClickProcessor().process(event)
#!/bin/bash

# Create Kinesis Stream
aws kinesis create-stream \
    --stream-name click-stream \
    --shard-count 1 \
    --region us-east-1

# Create DynamoDB Table
aws dynamodb create-table \
    --table-name user-clicks \
    --attribute-definitions \
        AttributeName=user_id,AttributeType=S \
        AttributeName=timestamp,AttributeType=N \
    --key-schema \
        AttributeName=user_id,KeyType=HASH \
        AttributeName=timestamp,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --ttl-specification \
        Enabled=true,AttributeName=expiry_time \
    --region us-east-1

echo "Setup complete. Allow 1 minute for resources to initialize."
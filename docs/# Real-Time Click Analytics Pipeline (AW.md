# Real-Time Click Analytics Pipeline (AWS)

Ingest, process, and store user click events using AWS Kinesis, Lambda, and DynamoDB.

## 🌟 Features
- **Real-time processing**: Handle 100+ events/sec
- **Zero-cost architecture**: Uses AWS Free Tier
- **Auto-scaling**: Kinesis shards + DynamoDB on-demand
- **TTL cleanup**: Automatic data expiry in DynamoDB

## 🛠️ Prerequisites
- AWS account (Free Tier eligible)
- Python 3.9+
- AWS CLI configured (`aws configure`)

## 🚀 Quick Start
1. **Deploy infrastructure**:
   ```bash
   aws cloudformation deploy --template-file src/cloudformation.yaml --stack-name click-analytics
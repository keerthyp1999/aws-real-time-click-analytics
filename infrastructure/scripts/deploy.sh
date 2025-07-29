#!/bin/bash

# Package Lambda
cd src/lambda/processor
zip -r ../../../infrastructure/lambda-package.zip .
cd ../../..

# Deploy CloudFormation
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/pipeline.yaml \
    --stack-name realtime-click-pipeline \
    --capabilities CAPABILITY_IAM

echo "Deployment complete. Stream ARN:"
aws kinesis describe-stream --stream-name click-stream --query 'StreamDescription.StreamARN'
## Common Issues

### 1. Kinesis Write Throttling
**Symptoms**:
- `ProvisionedThroughputExceededException` in producer logs
- High `WriteProvisionedThroughputExceeded` metrics

**Solutions**:
```bash
# Increase shard count
aws kinesis update-shard-count \
    --stream-name click-stream \
    --target-shard-count 2 \
    --scaling-type UNIFORM_SCALING
```

### 2. Lambda Timeouts
**Symptoms**:
- `Task timed out after 3.00 seconds` in CloudWatch

**Fix**:
```bash
aws lambda update-function-configuration \
    --function-name click-processor \
    --timeout 30
```
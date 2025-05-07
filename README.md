# Lambda benchmark

A prototype which implements a simple AWS Lambda function in several programming languages and benchmarks the relative performance.

## Lambda functionality

Each lambda implementation has the same functionality:

1. Read a batch of messages off an SQS queue
2. Validate the content of each message against the [shared JSON schema](./schema/event.json)
3. Write each message to a DynamoDB table with the partition key as the message's event ID and a TTL

## Requirements

- Node >= v20
- NPM
- OpenTofu (see `.opentofu-version`)
- Python
- Rust >= 1.80.0

## Deploying

The prototype is deployed with [OpenTofu](https://opentofu.org/).
Valid AWS credentials must be present in your shell.

First, build the lambda:

```bash
cd lambda/typescript
npm run build

```

Then deploy:

```bash
cd infra
tofu init
tofu apply
```

## Analysing the data

Install the Python requirements and run the script to download the report data from Cloudwatch:

```bash
cd benchmark/scripts
pip install -r requirements.txt
python download_log_data.py
```

This will save a CSV of the results in `benchmark/data`

# Lambda benchmark

A prototype which implements a simple AWS Lambda function in several programming languages and benchmarks the relative performance.

Each lambda implementation has the same functionality:

1. Read a batch of messages off an SQS queue
2. Validate the content of each message against the [shared JSON schema](./schema/event.json)
3. Write each message to a DynamoDB table with the partition key as the message's event ID and a TTL

The benchmark is designed to replicate real world use as much as possible.
The messages are sent to SQS in as close to one go as possible which means the lambdas are all running at the same time.
They all share the same DynamoDB table so need to compete for read resource.
The DynamoDB table has a randomly generated partition key to avoid 'hot' partitions.
Each Lambda function bundles the minimal dependencies - usually just a library for JSON Schema validation and the necessary AWS / runtime dependencies.

One of my colleagues has [extended the prototype](https://github.com/bmcgavin/lambda-benchmark) to also test Java through GraalVM.

## Requirements

- Node >= v20
- NPM
- OpenTofu (see `.opentofu-version`)
- Python
- Rust >= 1.80.0
- Ruby

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

## Benchmarking and analysing the data

Install the Python requirements and run the script to send events to the Lambdas:

```bash
cd benchmark/scripts
pip install -r requirements.txt
python run_load_test.py
```

Then wait 5 minutes for Cloudwatch to process the logs before downloading them:

```bash
python download_log_data.py
```

Finally, run the analysis script.
This will print summary data to your terminal and save plots in `/benchmark/scripts/plots`.

```bash
python analyse_results.py
```

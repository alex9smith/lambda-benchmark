# Lambda benchmark

A prototype which implements a simple AWS Lambda function in several programming languages and benchmarks the relative performance.

## Lambda functionality

Each lambda implementation has the same functionality:

1. Read a batch of messages off an SQS queue
2. Validate the content of each message against the [shared JSON schema](./schema/event.json)
3. Write each message to a DynamoDB table with the partition key as the message's event ID and a TTL

## Requirements

Node >= v 20
NPM
ESBuild availble globally

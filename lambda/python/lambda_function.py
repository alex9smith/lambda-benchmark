import json
from os import environ
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from jsonschema import Draft7Validator

logger = Logger()

validator = Draft7Validator(
    schema={
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "eventId": {"type": "string", "maxLength": 128},
            "emitterCode": {"type": "integer", "minimum": 0, "maximum": 100},
            "action": {
                "type": "string",
                "enum": ["sign_in", "sign_out", "create_account", "delete_account"],
            },
            "user": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "maxLength": 128},
                    "sessionId": {"type": "string", "maxLength": 128},
                    "deviceId": {"type": "string", "maxLength": 128},
                },
                "required": ["id", "sessionId"],
            },
        },
        "required": ["eventId", "emitterCode", "action", "user"],
    }
)

client = boto3.resource("dynamodb")
table = client.Table(environ["TABLE_NAME"])  # type: ignore


def write_to_dynamodb(event: dict) -> None:
    table.put_item(Item=event)


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> None:
    for record in event["Records"]:
        body = json.loads(record["body"])
        validator.validate(body)
        write_to_dynamodb(body)

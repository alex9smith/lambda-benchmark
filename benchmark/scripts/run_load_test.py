from enum import Enum, auto
from typing import TypedDict
from uuid import uuid4
import json
import boto3

MAX_BATCH_SIZE = 10  # 10 is the limit on the SQS SendMessageBatch API
EVENTS_PER_LAMBDA = 3000


class LiveLambdas(Enum):
    typescript = auto()
    rust = auto()
    ruby = auto()
    python = auto()
    java = auto()
    graalvm = auto()


class User(TypedDict):
    id: str
    sessionId: str
    deviceId: str


class Event(TypedDict):
    eventId: str
    action: str
    emitterCode: int
    user: User


class SQSMessage(TypedDict):
    Id: str
    MessageBody: str


def get_queue(client, language: LiveLambdas) -> str:
    return client.get_queue_by_name(
        QueueName=f"benchmark_lambda_{language.name}_queue",
    )


def generate_id() -> str:
    return str(uuid4())


def generate_event():
    return Event(
        eventId=generate_id(),
        action="sign_in",
        emitterCode=1,
        user=User(id=generate_id(), sessionId=generate_id(), deviceId=generate_id()),
    )


def generate_message() -> SQSMessage:
    return SQSMessage(
        Id=generate_id(),
        MessageBody=json.dumps(generate_event()),
    )


def send_events_to_queue(queue, num_events: int) -> None:
    events = [generate_message() for _ in range(num_events)]
    chunks = [
        events[i : i + MAX_BATCH_SIZE] for i in range(0, num_events, MAX_BATCH_SIZE)
    ]
    for chunk in chunks:
        queue.send_messages(Entries=chunk)


if __name__ == "__main__":
    sqs = boto3.resource("sqs")

    for language in LiveLambdas:
        print(f"Running for {language.name}")
        queue = get_queue(client=sqs, language=language)
        print("Got queue resource. Sending events")
        send_events_to_queue(queue=queue, num_events=EVENTS_PER_LAMBDA)
        print("Sent events")

from typing import List, TypedDict, Optional
from datetime import datetime, timedelta, timezone
from time import sleep, time
from csv import DictWriter
import re
import boto3

LIVE_LAMBDAS = ["typescript"]


class Row(TypedDict):
    timestamp: str
    message: str


class InvocationSummary(TypedDict):
    name: str
    execution_time_ms: float
    cold_start: bool
    init_duration_ms: Optional[float]


def submit_logs_query(client, lambda_name: str) -> str:
    finish = datetime.now(tz=timezone.utc)
    start = datetime.now(tz=timezone.utc) - timedelta(hours=1)

    response = client.start_query(
        logGroupName=f"/aws/lambda/{lambda_name}",
        startTime=int(start.timestamp()),
        endTime=int(finish.timestamp()),
        queryString="fields @timestamp, @message",
        limit=10000,
    )

    return response["queryId"]


def poll_for_query_result(client, query_id: str):
    results = client.get_query_results(queryId=query_id)
    while results["status"] not in [
        "Complete",
        "Failed",
        "Cancelled",
        "Timeout",
        "Unknown",
    ]:
        print(f"Query ID {query_id} not ready. Waiting")
        sleep(10)
        results = client.get_query_results(queryId=query_id)

    return results.get("results", [])


def parse_result_row(row) -> Row:
    result = Row(timestamp="", message="")
    for field in row:
        if field["field"] == "@timestamp":
            result["timestamp"] = field["value"]
        elif field["field"] == "@message":
            result["message"] = field["value"]

    return result


def process_report_rows(rows: List[Row], name: str) -> List[InvocationSummary]:
    result = []
    for row in rows:
        if row["message"].startswith("REPORT"):
            result.append(calc_report_summary(row["message"], name))

    return result


def calc_report_summary(message: str, name: str) -> InvocationSummary:
    cold_start = False
    init_duration_ms = None
    if init_match := re.search(
        r"Init Duration: (\d*\.?\d+) ms", message, re.IGNORECASE
    ):
        init_duration_ms = float(init_match.group(1))
        cold_start = True

    if exec_match := re.search(
        r"Billed Duration: (\d*\.?\d+) ms", message, re.IGNORECASE
    ):
        return InvocationSummary(
            name=name,
            execution_time_ms=float(exec_match.group(1)),
            cold_start=cold_start,
            init_duration_ms=init_duration_ms,
        )

    print(f"Malformed message: {message}")
    raise ValueError("Malformed message")


def write_to_csv(data):
    with open("../data/parsed_cloudwatch_logs.csv", "w") as f:
        writer = DictWriter(
            f,
            fieldnames=["name", "execution_time_ms", "cold_start", "init_duration_ms"],
        )
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    logs_client = boto3.client("logs")
    print("Submitting queries")
    queries = [
        (submit_logs_query(logs_client, f"lambda_benchmark_{name}_lambda"), name)
        for name in LIVE_LAMBDAS
    ]
    sleep(1)

    raw_results = {}
    for query_id, name in queries:
        print(f"Querying results for {name}")
        raw_results[name] = poll_for_query_result(logs_client, query_id)

    parsed: List[InvocationSummary] = []
    for name, results in raw_results.items():
        rows = [parse_result_row(row) for row in results]
        for report in process_report_rows(rows, name):
            parsed.append(report)

    write_to_csv(parsed)

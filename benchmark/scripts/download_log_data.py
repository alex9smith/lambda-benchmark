from typing import List, TypedDict, Optional
from datetime import datetime, timedelta, timezone
from time import sleep
from csv import DictWriter
import re
import boto3

from run_load_test import LiveLambdas


class Row(TypedDict):
    timestamp: str
    message: str


class InvocationSummary(TypedDict):
    name: str
    request_id: str
    execution_time_ms: float
    cold_start: bool
    init_duration_ms: Optional[float]


def get_error_request_id(line: str) -> str:
    if id_match := re.search(r"\s(.*?)\sERROR", line, re.IGNORECASE):
        return id_match.group(1)
    else:
        raise ValueError(f"Could not find request ID in error line: {line}")


class LogReportBuilder:
    def __init__(self, client):
        self.client = client
        self.queries = []
        self.failed_requests = []

    def submit_logs_query(self, lambda_name: str):
        finish = datetime.now(tz=timezone.utc)
        start = datetime.now(tz=timezone.utc) - timedelta(hours=6)

        response = self.client.start_query(
            logGroupName=f"/aws/lambda/lambda_benchmark_{lambda_name}_lambda",
            startTime=int(start.timestamp()),
            endTime=int(finish.timestamp()),
            queryString="fields @timestamp, @message",
            limit=10000,
        )

        self.queries.append((response["queryId"], lambda_name))

    def poll_for_all_query_results(self):
        all_results = {}
        for query_id, name in self.queries:
            print(f"Querying results for {name}")
            results = self.client.get_query_results(queryId=query_id)
            while results["status"] not in [
                "Complete",
                "Failed",
                "Cancelled",
                "Timeout",
                "Unknown",
            ]:
                print(f"Query ID {query_id} not ready. Waiting")
                sleep(10)
                results = self.client.get_query_results(queryId=query_id)

            all_results[name] = results.get("results", [])
        return all_results

    def parse_result_row(self, row) -> Row:
        result = Row(timestamp="", message="")
        for field in row:
            if field["field"] == "@timestamp":
                result["timestamp"] = field["value"]
            elif field["field"] == "@message":
                result["message"] = field["value"]

        return result

    def process_report_rows(
        self, rows: List[Row], name: str
    ) -> List[InvocationSummary]:
        result = []
        for row in rows:
            if row["message"].startswith("REPORT"):
                result.append(self.calc_report_summary(row["message"], name))
            elif "ERROR	Invoke Error" in row["message"]:
                self.failed_requests.append(get_error_request_id(row["message"]))

        return result

    def calc_report_summary(self, message: str, name: str) -> InvocationSummary:
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

            if id_match := re.search(
                r"RequestId: (.*?)(?:\s|\\t)", message, re.IGNORECASE
            ):
                return InvocationSummary(
                    request_id=id_match.group(1),
                    name=name,
                    execution_time_ms=float(exec_match.group(1)),
                    cold_start=cold_start,
                    init_duration_ms=init_duration_ms,
                )

        print(f"Malformed message: {message}")
        raise ValueError("Malformed message")

    def remove_failed_requests(
        self, rows: List[InvocationSummary]
    ) -> List[InvocationSummary]:
        failed_requests = set(self.failed_requests)
        print(f"Found {len(failed_requests)} failed requests")
        return [s for s in rows if s["request_id"] not in failed_requests]

    def build_report(self) -> List[InvocationSummary]:
        for name in LiveLambdas:
            print(f"Submitting query for {name.name} Lambda")
            self.submit_logs_query(name.name)

        sleep(2)
        raw_results = self.poll_for_all_query_results()

        print("Processing downloaded data")
        parsed: List[InvocationSummary] = []
        for name, results in raw_results.items():
            rows = [builder.parse_result_row(row) for row in results]
            for report in builder.process_report_rows(rows, name):
                parsed.append(report)

        print("Removing failed requests")
        return builder.remove_failed_requests(parsed)


def write_to_csv(data):
    with open("../data/parsed_cloudwatch_logs.csv", "w") as f:
        writer = DictWriter(
            f,
            fieldnames=[
                "name",
                "request_id",
                "execution_time_ms",
                "cold_start",
                "init_duration_ms",
            ],
        )
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    builder = LogReportBuilder(boto3.client("logs"))
    report = builder.build_report()
    write_to_csv(report)

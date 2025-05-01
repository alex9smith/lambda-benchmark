resource "aws_sqs_queue" "typescript_lambda_queue" {
  name_prefix = "benchmark_lambda_typescript_queue"
  tags        = var.default_tags
}

resource "aws_sqs_queue" "queue" {
  name = "benchmark_lambda_${var.language_name}_queue"
  tags = var.default_tags
}

resource "aws_cloudwatch_log_group" "lambda_benchmark_typescript_logs" {
  name              = "/aws/lambda/lambda_benchmark_typescript_lambda"
  retention_in_days = 3
  tags              = var.default_tags
}

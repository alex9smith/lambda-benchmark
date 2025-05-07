resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/aws/lambda/lambda_benchmark_${var.language_name}_lambda"
  retention_in_days = 3
  tags              = var.default_tags
}

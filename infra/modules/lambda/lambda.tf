resource "aws_lambda_function" "lambda" {
  function_name                  = "lambda_benchmark_${var.language_name}_lambda"
  filename                       = var.source_file
  role                           = aws_iam_role.base_lambda_role.arn
  handler                        = var.handler
  source_code_hash               = filebase64sha256(var.source_file)
  runtime                        = var.runtime
  architectures                  = ["arm64"]
  timeout                        = var.timeout
  tags                           = var.default_tags
  # reserved  _concurrent_executions = 1
  memory_size                    = var.lambda_memory

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name,
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.allow_logging,
    aws_cloudwatch_log_group.log_group,
  ]
}

resource "aws_lambda_event_source_mapping" "mapping" {
  event_source_arn = aws_sqs_queue.queue.arn
  function_name    = aws_lambda_function.lambda.arn
  batch_size       = 5
}

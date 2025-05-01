resource "aws_lambda_function" "lambda_benchmark_typescript_lambda" {
  function_name    = "lambda_benchmark_typescript_lambda"
  filename         = "../lambda/typescript/dist/index.zip"
  role             = aws_iam_role.lambda_benchmark_lambda_role.arn
  handler          = "index.handler"
  source_code_hash = filebase64sha256("../lambda/typescript/dist/index.zip")
  runtime          = "nodejs20.x"
  architectures    = ["arm64"]
  timeout          = 5
  tags             = var.default_tags

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name,
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_benchmark_allow_logging,
    aws_cloudwatch_log_group.lambda_benchmark_typescript_logs,
  ]
}

resource "aws_lambda_event_source_mapping" "lambda_benchmark_typescript_lambda" {
  event_source_arn = aws_sqs_queue.typescript_lambda_queue.arn
  function_name    = aws_lambda_function.lambda_benchmark_typescript_lambda.arn
}

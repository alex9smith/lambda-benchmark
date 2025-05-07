data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "base_lambda_role" {
  name               = "lambda_benchmark_base_${var.language_name}_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  tags               = var.default_tags
}

data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "allow_logging" {
  name        = "lambda_benchmark_${var.language_name}_allow_logging"
  path        = "/"
  description = "Allow the ${var.language_name} lambda in the lambda_benchmark app to log to Cloudwatch"
  policy      = data.aws_iam_policy_document.lambda_logging.json
  tags        = var.default_tags
}

resource "aws_iam_role_policy_attachment" "allow_logging" {
  role       = aws_iam_role.base_lambda_role.name
  policy_arn = aws_iam_policy.allow_logging.arn
}

data "aws_iam_policy_document" "dynamodb_access" {
  statement {
    effect = "Allow"

    actions = [
      "dynamodb:PutItem",
    ]

    resources = ["arn:aws:dynamodb:*:*:table/${var.dynamodb_table_name}"]
  }
}


resource "aws_iam_policy" "dynamodb_access" {
  name        = "lambda_benchmark_${var.language_name}_dynamodb_access"
  path        = "/"
  description = "IAM policy to allow the ${var.language_name} lambda in the lambda_benchmark app to write to DynamoDB"
  policy      = data.aws_iam_policy_document.dynamodb_access.json
  tags        = var.default_tags
}

resource "aws_iam_role_policy_attachment" "dynamodb_access" {
  role       = aws_iam_role.base_lambda_role.name
  policy_arn = aws_iam_policy.dynamodb_access.arn
}

data "aws_iam_policy_document" "sqs_access" {
  statement {
    sid       = "AllowSQSPermissions"
    effect    = "Allow"
    resources = [aws_sqs_queue.queue.arn]

    actions = [
      "sqs:ChangeMessageVisibility",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:ReceiveMessage",
    ]
  }

}

resource "aws_iam_policy" "sqs_access" {
  name        = "lambda_benchmark_${var.language_name}_sqs_access"
  path        = "/"
  description = "IAM policy to allow the ${var.language_name} lambda in the lambda_benchmark app to read from SQS"
  policy      = data.aws_iam_policy_document.sqs_access.json
  tags        = var.default_tags
}

resource "aws_iam_role_policy_attachment" "sqs_access" {
  role       = aws_iam_role.base_lambda_role.name
  policy_arn = aws_iam_policy.sqs_access.arn
}

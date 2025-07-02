module "typescript_lambda" {
  source = "../modules/lambda"

  source_file         = "../../../lambda/typescript/dist/index.zip"
  language_name       = "typescript"
  runtime             = "nodejs20.x"
  handler             = "index.handler"
  dynamodb_table_name = var.dynamodb_table_name
  arch                = var.arch
  reserved_concurrent_executions = var.reserved_concurrent_executions
}

module "rust_lambda" {
  source = "../modules/lambda"

  source_file         = "../../../lambda/rust/target/lambda/rust/bootstrap.zip"
  language_name       = "rust"
  runtime             = "provided.al2023"
  handler             = "bootstrap"
  dynamodb_table_name = var.dynamodb_table_name
  arch                = var.arch
  reserved_concurrent_executions = var.reserved_concurrent_executions
}

module "ruby_lambda" {
  source = "../modules/lambda"

  source_file         = "../../../lambda/ruby/deploy.zip"
  language_name       = "ruby"
  runtime             = var.ruby_runtime
  handler             = "lambda_function.Lambda::Handler.process"
  dynamodb_table_name = var.dynamodb_table_name
  arch                = var.arch
  reserved_concurrent_executions = var.reserved_concurrent_executions
}

module "python_lambda" {
  source = "../modules/lambda"

  source_file         = "../../../lambda/python/deploy.zip"
  language_name       = "python"
  runtime             = "python3.12"
  handler             = "lambda_function.handler"
  dynamodb_table_name = var.dynamodb_table_name
  arch                = var.arch
  reserved_concurrent_executions = var.reserved_concurrent_executions
}

module "java_lambda" {
  source = "../modules/lambda"

  source_file         = "../../../lambda/java/JavaLambda/target/JavaLambda.jar"
  language_name       = "java"
  runtime             = "java21"
  handler             = "alex9smith.App::handleRequest"
  dynamodb_table_name = var.dynamodb_table_name
  timeout             = 10
  arch                = var.arch
  reserved_concurrent_executions = var.reserved_concurrent_executions
}

module "graalvm_lambda" {
  source = "../modules/lambda"

  source_file         = "../../../lambda/graalvm/GraalVMLambda/target/function-${var.arch}.zip"
  language_name       = "graalvm"
  runtime             = "provided.al2023"
  handler             = "alex9smith.App::handleRequest"
  dynamodb_table_name = var.dynamodb_table_name
  timeout             = 10
  arch                = var.arch
  reserved_concurrent_executions = var.reserved_concurrent_executions
}

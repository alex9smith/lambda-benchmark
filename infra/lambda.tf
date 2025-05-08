module "typescript_lambda" {
  source = "./modules/lambda"

  source_file         = "../lambda/typescript/dist/index.zip"
  language_name       = "typescript"
  runtime             = "nodejs20.x"
  handler             = "index.handler"
  dynamodb_table_name = var.dynamodb_table_name
}

module "rust_lambda" {
  source = "./modules/lambda"

  source_file         = "../lambda/rust/target/lambda/rust/bootstrap.zip"
  language_name       = "rust"
  runtime             = "provided.al2023"
  handler             = "bootstrap"
  dynamodb_table_name = var.dynamodb_table_name
}

module "ruby_lambda" {
  source = "./modules/lambda"

  source_file         = "../lambda/ruby/deploy.zip"
  language_name       = "ruby"
  runtime             = "ruby3.3"
  handler             = "lambda_function.Lambda::Handler.process"
  dynamodb_table_name = var.dynamodb_table_name
}

module "typescript_lambda" {
  source = "./modules/lambda"

  source_file         = "../lambda/typescript/dist/index.zip"
  language_name       = "typescript"
  runtime             = "nodejs20.x"
  handler             = "index.handler"
  dynamodb_table_name = var.dynamodb_table_name
}

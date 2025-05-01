resource "aws_dynamodb_table" "table" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "eventId"
  tags         = var.default_tags

  attribute {
    name = "eventId"
    type = "S"
  }

}

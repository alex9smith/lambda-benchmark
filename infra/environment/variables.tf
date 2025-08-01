variable "application_name" {
  type    = string
  default = "Lambda benchmark prototype"
}

variable "dynamodb_table_name" {
  type    = string
  default = "lambda_benchmark"
}

variable "owner" {
  type = string
}

variable "default_tags" {
  description = "Tags to apply to AWS resources"
  default = {
    Environment = "Dev"
    Application = "Lambda benchmark prototype"
  }
}

variable "arch" {
  type = string
  default = "arm64"
}

variable "ruby_runtime" {
  type = string
  default = "ruby3.3"
}

variable "reserved_concurrent_executions" {
  type = number
  default = 20
}

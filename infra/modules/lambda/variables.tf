variable "language_name" {
  type = string
}

variable "source_file" {
  type = string
}

variable "handler" {
  type = string
}

variable "runtime" {
  type = string
}

variable "dynamodb_table_name" {
  type = string
}

variable "lambda_memory" {
  type    = number
  default = 256
}

variable "timeout" {
  type    = number
  default = 5
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

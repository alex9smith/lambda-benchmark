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

variable "default_tags" {
  description = "Tags to apply to AWS resources"
  default = {
    Environment = "Dev"
    Application = "Lambda benchmark prototype"
  }
}


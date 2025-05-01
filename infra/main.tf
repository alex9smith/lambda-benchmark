terraform {
  required_providers {
    aws = {
      source  = "opentofu/aws"
      version = "5.69.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

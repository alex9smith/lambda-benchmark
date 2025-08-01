locals {

}

module "environment" {
  source = "../../environment"

  owner = var.owner
  arch = "arm64"
  ruby_runtime = "ruby3.2"
}
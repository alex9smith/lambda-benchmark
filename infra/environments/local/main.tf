locals {

}

module "environment" {
  source = "../../environment"

  owner = var.owner
  arch = "x86_64"
  ruby_runtime = "ruby3.2"
}
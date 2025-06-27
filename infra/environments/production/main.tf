locals {

}

module "environment" {
  source = "../../environment"

  owner = var.owner
  arch = "arm64"
}
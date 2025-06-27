locals {

}

module "environment" {
  source = "../../environment"

  owner = var.owner
  arch = "x86_64"
}
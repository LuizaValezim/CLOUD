data "aws_instances" "instances" {
  instance_state_names = ["running", "stopped"]

}

data "aws_availability_zones" "available" {}


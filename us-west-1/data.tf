# data "aws_iam_users" "users" {}

data "aws_instances" "instances" {
  instance_state_names = ["running", "stopped"]
}
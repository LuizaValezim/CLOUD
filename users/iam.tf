
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_iam_user" "user" {
  for_each = {for user in var.aws_user_name : user.username => user}
  name = each.value.username

  tags = {
    tag-key = "created-user"
  }
}

resource "aws_iam_access_key" "user" {
  for_each = {for user in var.aws_user_name : user.username => user}
  user = aws_iam_user.user[each.value.username].name
}

resource "aws_iam_user_login_profile" "profile" {
  for_each               = {for user in var.aws_user_name: user.username => user}
  user                    =  aws_iam_user.user[each.value.username].name
  password_reset_required =  true
  password_length         =  10   
}

resource "aws_iam_policy" "start_stop" {
  name        = "StartStopInstances"
  path        = "/"
  description = "Permite user iniciar e parar instancias"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            "Sid": "FirstStatement",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "arn:aws:ec2:*:116979769772:instance/*"
        },
        {
            "Sid": "SecondStatement",
            "Effect": "Allow",
            "Action": "ec2:DescribeInstances",
            "Resource": "*"
        }
    ]
  })
}


resource "aws_iam_policy" "change_pass" {
  name        = "ChangePassword"
  path        = "/"
  description = "Permite user trocar senha"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            "Sid": "FirstStatement",
            "Effect": "Allow",
            "Action": "iam:ChangePassword",
            "Resource": "arn:aws:iam::116979769772:user/*"
        }
    ]  
  })
}

resource "aws_iam_policy" "niveis" {
  for_each = {for user in var.aws_user_name: user.username => user}
  name        = each.value.policy_name
  path        = "/"
  description = each.value.policy_description

  policy = jsonencode({
    "Version" = "2012-10-17"
    "Statement" = [
        {
            "Effect" = each.value.policy_effect
            "Action" = each.value.policy_action
            "Resource" = each.value.policy_resource
        }
    ]
})
}

resource "aws_iam_user_policy_attachment" "attach" {
    for_each = {for user in var.aws_user_name: user.username => user}
    user       = aws_iam_user.user[each.value.username].name
    policy_arn =  aws_iam_policy.start_stop.arn
}

resource "aws_iam_user_policy_attachment" "attach2" {
    for_each = {for user in var.aws_user_name: user.username => user}
    user       = aws_iam_user.user[each.value.username].name
    policy_arn       = aws_iam_policy.change_pass.arn
}

resource "aws_iam_user_policy_attachment" "user_policy_attachment" {
    for_each = {for user in var.aws_user_name: user.username => user}
    user       = aws_iam_user.user[each.value.username].name
    policy_arn =  aws_iam_policy.niveis[each.value.username].arn
}
output "password" {
//    sensitive = true
    value = values({ for user_test, profile in aws_iam_user_login_profile.profile : user_test => profile})
}

output "aws_iam_users" {
    value = data.aws_iam_users.users
}
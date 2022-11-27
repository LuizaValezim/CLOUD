# output "password" {
# //    sensitive = true
#     value = values({ for user_test, profile in aws_iam_user_login_profile.profile : user_test => profile})
# }


output "nome_instancia_region" {
    value = [for key, value in aws_instance.app_server : "nome: ${key}| id: ${value.id} - ${value.availability_zone}"]
  
}

output "instances" {
    value = data.aws_instances.instances
}

output "sec_group_name" {
    value = [for key, value in aws_security_group.allow : [for rule in value.ingress: "nome: ${key} - description: ${rule.description} - from_port: ${rule.from_port} - to_port: ${rule.to_port} - protocol: ${rule.protocol} - cidr_blocks: ${rule.cidr_blocks[0]}"]]
}


# output "aws_iam_users" {
#     value = data.aws_iam_users.users
# }
  

    
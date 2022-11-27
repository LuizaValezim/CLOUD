
variable "aws_user_name" {
  type        = list(object({
    username = string
    policy_name = string
    policy_description = string
    policy_action = list(string)
    policy_resource = string
    policy_effect = string
  }))
  description = "Nome do usuário da AWS para ser usado no servidor."
}


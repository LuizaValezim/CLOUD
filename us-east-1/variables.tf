variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "A região da AWS para fazer o deploy do servidor."
}

variable "vpc_cidr_block" {
  type        = string
  default     =  "10.0.0.0/16"
}

variable "virtual_machines" {
  description = "Informações sobre cada máquina a ser criada"
  type = map(object({
    image_id = string
    instance_type = string
  }))
}

variable "sec_groups"{
  description = "Informações sobre cada grupo de segurança a ser criado"
  type = map(object({
    name = string
    ingress = list(map(object({
      description = string
      from_port = number
      ipv6_cidr_blocks = list(string)
      prefix_list_ids = list(string)
      to_port = number
      protocol = string
      security_groups = list(string)
      self = bool
      cidr_blocks = list(string)
    })))
  }))
}


variable "sec_group_instances" {
  type = map(object({
    sec_names = list(string)
  }))
  description = "nome dos grupos de segurança para instâncias"
}

  
variable "pgp_key" {
  default = <<EOF
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
EOF
  
}

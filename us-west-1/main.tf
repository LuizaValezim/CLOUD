# VPC criação de uma VPC e sub-rede; instâncias: esta funcionalidade deverá permitir a escolha de pelo menos 2 tipos de configuração de hosts;
# ainda deverá ser possível parar e iniciar as instâncias; security group: criação e a associação de grupos de segurança com instâncias; Usuário no IAM.


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# Prover as credenciais da AWS
provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  cidr_block       =    var.vpc_cidr_block        #"172.16.0.0/16"
  instance_tenancy = "default"

  tags = {
    name = "VPC${var.aws_region}"
  }
}

# Subnet publica
resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  #cidr_block =  aws_vpc.main.cidr_block             #"172.16.1.0/24"
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, 1)  # Pega o cidr do block da vpc e divide em 2
  map_public_ip_on_launch = true

  tags = {
    Name = "Subnet"
  }
}
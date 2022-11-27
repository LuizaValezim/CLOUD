
resource "aws_security_group" "allow" {
  for_each = var.sec_groups
  name        = each.value.name
  vpc_id      = aws_vpc.main.id

    ingress = [for rule in each.value.ingress : rule.ingress]
  
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        name        = "security_group"
    }
    depends_on      = [aws_vpc.main]

}






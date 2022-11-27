resource "aws_instance" "app_server" {
  for_each = var.virtual_machines
  ami           =  each.value.image_id  # Ubuntu Server 20.04 LTS (HVM), SSD Volume Type var.image_id
  instance_type =  each.value.instance_type  #var.aws_instance_type
  key_name = "luizavap"
  subnet_id = aws_subnet.main.id
  # subnet_id = aws_subnet.public.id
  vpc_security_group_ids = [for sec_name in var.sec_group_instances[each.key].sec_names : aws_security_group.allow[sec_name].id]

  tags = {
    Name = "${each.key}"
    # Owner = "${var.aws_user_name}"
  }

#   depends_on = [aws_key_pair.my_key]
}
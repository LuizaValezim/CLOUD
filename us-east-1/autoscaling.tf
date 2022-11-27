
resource "aws_launch_configuration" "teste" {
  name_prefix     = "learn-terraform-aws-asg-"
  image_id        = "ami-0fb0bb0be0c875fa5"
  instance_type   = "t2.micro"
  key_name        = "luizavap"
  # user_data       = file("user-data.sh")
  security_groups = [aws_security_group.teste_instance.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "teste" {
  name                 = "teste"
  min_size             = 1
  max_size             = 3
  desired_capacity     = 1
  launch_configuration = aws_launch_configuration.teste.name
  vpc_zone_identifier  = ["${aws_subnet.public.id}", "${aws_subnet.private.id}"]

  tag {
    key                 = "Name"
    value               = "HashiCorp Learn ASG - Terramino"
    propagate_at_launch = true
  }
}

resource "aws_lb" "teste" {
  name               = "learn-asg-teste-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.teste_lb.id]
  subnets            = ["${aws_subnet.public.id}", "${aws_subnet.private.id}"]

}

resource "aws_lb_listener" "teste" {
  load_balancer_arn = aws_lb.teste.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.teste.arn
  }
}

resource "aws_lb_target_group" "teste" {
  name     = "learn-asg-teste"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}


resource "aws_autoscaling_attachment" "teste" {
  autoscaling_group_name = aws_autoscaling_group.teste.id
  lb_target_group_arn   = aws_lb_target_group.teste.arn
}

resource "aws_security_group" "teste_instance" {
  name = "learn-asg-teste-instance"
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.teste_lb.id]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.teste_lb.id]
  }

  vpc_id = aws_vpc.main.id
}

resource "aws_security_group" "teste_lb" {
  name = "learn-asg-teste-lb"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = aws_vpc.main.id
}


resource "aws_autoscaling_policy" "scale_down" {
  name                   = "terramino_scale_down"
  autoscaling_group_name = aws_autoscaling_group.teste.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = -1
  cooldown               = 120
}

resource "aws_cloudwatch_metric_alarm" "scale_down" {
  alarm_description   = "Monitors CPU utilization for Terramino ASG"
  alarm_actions       = [aws_autoscaling_policy.scale_down.arn]
  alarm_name          = "teste_scale_down"
  comparison_operator = "LessThanOrEqualToThreshold"
  namespace           = "AWS/EC2"
  metric_name         = "CPUUtilization"
  threshold           = "10"
  evaluation_periods  = "2"
  period              = "120"
  statistic           = "Average"

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.teste.name
  }
}


resource "aws_autoscaling_policy" "scale_up" {
  name                   = "terramino_scale_up"
  autoscaling_group_name = aws_autoscaling_group.teste.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = 1
  cooldown               = 120
}

resource "aws_cloudwatch_metric_alarm" "scale_up" {
  alarm_description   = "Monitors CPU utilization for Terramino ASG"
  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]
  alarm_name          = "teste_scale_up"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  namespace           = "AWS/EC2"
  metric_name         = "CPUUtilization"
  threshold           = "50"
  evaluation_periods  = "2"
  period              = "120"
  statistic           = "Average"

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.teste.name
  }
}
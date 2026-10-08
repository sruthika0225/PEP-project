# EC2 Instance
resource "aws_instance" "ec2" {
  ami           = "ami-0a29987e14ae814db"
  subnet_id     = aws_subnet.pub_subnet1.id
  instance_type = var.instance_type
  key_name = "pep-project"

  vpc_security_group_ids = [aws_security_group.sg.id]
  associate_public_ip_address = true

  user_data = file("${path.module}/user_data.yaml")

  tags = {
    Name = "sjce-devops"
    team = "sjce"
  }
}

# Security Group
resource "aws_security_group" "sg" {
  name        = "pep-remainder-sg"
  description = "Security group for Remainder App"
  vpc_id      = aws_vpc.pro_vpc.id

  tags = {
    Name = "Learn-SG"
  }
}

# SSH
resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
  security_group_id = aws_security_group.sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

# HTTP
resource "aws_vpc_security_group_ingress_rule" "allow_http" {
  security_group_id = aws_security_group.sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}

# HTTPS
resource "aws_vpc_security_group_ingress_rule" "allow_https" {
  security_group_id = aws_security_group.sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  ip_protocol       = "tcp"
  to_port           = 443
}

# Remainder App
resource "aws_vpc_security_group_ingress_rule" "allow_app" {
  security_group_id = aws_security_group.sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 5000
  ip_protocol       = "tcp"
  to_port           = 5000
}
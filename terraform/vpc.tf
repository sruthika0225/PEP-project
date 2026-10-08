# VPC
resource "aws_vpc" "pro_vpc" {
  cidr_block       = var.vpc_cidr
  instance_tenancy = "default"

  tags = {
    Name = "demovpc"
  }
}

# Get available Availability Zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Public Subnet 1
resource "aws_subnet" "pub_subnet1" {
  vpc_id                  = aws_vpc.pro_vpc.id
  cidr_block              = "11.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "Public Subnet 1"
  }
}

# Public Subnet 2
resource "aws_subnet" "pub_subnet2" {
  vpc_id                  = aws_vpc.pro_vpc.id
  cidr_block              = "11.0.2.0/24"
  availability_zone       = data.aws_availability_zones.available.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name = "Public Subnet 2"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.pro_vpc.id

  tags = {
    Name = "pro-vpc-igw"
  }
}

# Route Table
resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.pro_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "pro-vpc-rt"
  }
}

# Route Table Association - Public Subnet 1
resource "aws_route_table_association" "rta_pubsub1" {
  subnet_id      = aws_subnet.pub_subnet1.id
  route_table_id = aws_route_table.rt.id
}

# Route Table Association - Public Subnet 2
resource "aws_route_table_association" "rta_pubsub2" {
  subnet_id      = aws_subnet.pub_subnet2.id
  route_table_id = aws_route_table.rt.id
}
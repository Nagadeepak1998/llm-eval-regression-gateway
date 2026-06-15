provider "aws" {
  region = var.aws_region
}

resource "aws_ecr_repository" "app" {
  name = var.project_name
}

resource "aws_ecs_cluster" "app" {
  name = "${var.project_name}-cluster"
}

resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 14
}

resource "aws_security_group" "app" {
  name        = "${var.project_name}-sg"
  description = "Access for the llm eval gateway"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


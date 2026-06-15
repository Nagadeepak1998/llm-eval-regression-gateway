variable "aws_region" {
  type = string
}

variable "project_name" {
  type    = string
  default = "llm-eval-regression-gateway"
}

variable "image_uri" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "vpc_id" {
  type = string
}

variable "allowed_cidr" {
  type = string
}


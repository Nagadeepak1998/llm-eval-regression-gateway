variable "aws_region" {
  type        = string
  description = "AWS region for ECS resources."
  default     = "us-east-1"
}

variable "app_name" {
  type        = string
  description = "Application name prefix."
  default     = "llm-eval-regression-gateway"
}

variable "container_image" {
  type        = string
  description = "Container image URI."
}

variable "subnet_ids" {
  type        = list(string)
  description = "Public subnet IDs for the service."
}

variable "vpc_id" {
  type        = string
  description = "VPC ID for the service."
}


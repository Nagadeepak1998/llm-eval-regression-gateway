# Terraform Notes

This skeleton provisions an ECS Fargate service, CloudWatch log group, security group,
and execution role for the gateway.

```bash
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
```

Use a private load balancer, WAF, and auth layer before treating the service as production-ready.


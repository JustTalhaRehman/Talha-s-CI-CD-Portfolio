variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "project" {
  description = "Project name"
  type        = string
  default     = "myapp"
}

variable "tf_state_bucket" {
  description = "S3 bucket for Terraform state"
  type        = string
  default     = "talha-terraform-state"
}

variable "tf_state_key" {
  description = "Terraform state file key"
  type        = string
  default     = "production/terraform.tfstate"
}

variable "tf_dynamodb_table" {
  description = "DynamoDB table for Terraform locks"
  type        = string
  default     = "terraform-locks"
}

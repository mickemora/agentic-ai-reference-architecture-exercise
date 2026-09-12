terraform {
  required_version = ">= 1.8"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = "agentic-ai-reference-architecture-exercise"
      ManagedBy = "Terraform"
      DataClass = "Synthetic"
    }
  }
}

# Resources will be added incrementally in the phase that introduces each AWS capability.

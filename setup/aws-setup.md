# AWS Setup Guide

## Prerequisites
- AWS CLI installed and configured
- IAM permissions to create roles and policies

## Step 1: Create Terraform Backend Resources

### S3 Bucket for State Storage
```bash
aws s3api create-bucket \
  --bucket myapp-terraform-state \
  --region us-east-2 \
  --create-bucket-configuration LocationConstraint=us-east-2

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket myapp-terraform-state \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket myapp-terraform-state \
  --server-side-encryption-configuration '{
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        }
      }
    ]
  }'

# Block public access
aws s3api put-public-access-block \
  --bucket myapp-terraform-state \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### DynamoDB Table for State Locking
```bash
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-2
```

## Step 2: Create GitHub Actions OIDC Provider

```bash
# Create OIDC provider for GitHub
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

## Step 3: Create IAM Roles for GitHub Actions

### Staging Role
```bash
# Create trust policy
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:JustTalhaRehman/Talha-s-CI-CD-Portfolio:ref:refs/heads/main"
        }
      }
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name github-actions-staging-role \
  --assume-role-policy-document file://trust-policy.json \
  --description "GitHub Actions staging role"

# Attach policies (adjust permissions as needed)
aws iam attach-role-policy \
  --role-name github-actions-staging-role \
  --policy-arn arn:aws:policy/PowerUserAccess

aws iam attach-role-policy \
  --role-name github-actions-staging-role \
  --policy-arn arn:aws:policy/AmazonEC2ContainerRegistryFullAccess
```

### Production Role
```bash
# Create production role
aws iam create-role \
  --role-name github-actions-production-role \
  --assume-role-policy-document file://trust-policy.json \
  --description "GitHub Actions production role"

# Attach policies (more restrictive for production)
aws iam attach-role-policy \
  --role-name github-actions-production-role \
  --policy-arn arn:aws:policy/AmazonEC2ContainerRegistryFullAccess

# Add EKS permissions
aws iam attach-role-policy \
  --role-name github-actions-production-role \
  --policy-arn arn:aws:policy/AmazonEKSClusterPolicy
```

## Step 4: Get Role ARNs
```bash
# Get the ARNs to add to GitHub secrets
aws iam get-role --role-name github-actions-staging-role --query Role.Arn --output text
aws iam get-role --role-name github-actions-production-role --query Role.Arn --output text
```

## Step 5: Configure GitHub Secrets

Go to your GitHub repository settings and add these secrets:

| Secret | Value |
|--------|-------|
| `AWS_ACCOUNT_ID` | Your AWS Account ID |
| `AWS_OIDC_ROLE` | ARN of staging role |
| `AWS_PROD_OIDC_ROLE` | ARN of production role |
| `SLACK_WEBHOOK` | Your Slack webhook URL |

## Step 6: Create GitHub Environments

1. Go to Settings > Environments
2. Create `staging` environment
3. Create `production` environment with protection rules:
   - Required reviewers: 1
   - Wait timer: 5 minutes

## Verification

Test the setup by:
1. Running `terraform init` in the terraform directory
2. Creating a pull request to trigger the infrastructure pipeline
3. Pushing to main to trigger the full CI/CD pipeline

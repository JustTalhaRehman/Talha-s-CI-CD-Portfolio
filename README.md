# Production-Grade CI/CD Pipeline created by Talha
Production-grade CI/CD pipeline with GitHub Actions — automated testing, security scanning, Docker builds, canary deployments to EKS, and Terraform infrastructure management for AWS.

End-to-end CI/CD and Infrastructure-as-Code pipeline built with GitHub Actions, Terraform, Kubernetes, and AWS.

## What's Included

### CI/CD Pipeline (`.github/workflows/ci.yml`)

Automated application delivery pipeline with 5 stages:

| Stage | What It Does |
|-------|-------------|
| **Lint & Format** | Code quality checks with Ruff |
| **Test** | Unit & integration tests with PostgreSQL and Redis service containers, coverage reporting |
| **Security Scan** | Filesystem vulnerability scanning with Trivy, results uploaded to GitHub Security tab |
| **Build & Push** | Multi-stage Docker build, push to ECR with SBOM and provenance, image vulnerability scan |
| **Deploy** | Canary deployment to Staging → smoke tests → promote → Production with manual approval |

**Trigger:** Runs on every pull request (lint, test, security). Build and deploy only on merge to `main`.

### Infrastructure Pipeline (`.github/workflows/iac-pipeline.yml`)

GitOps-driven infrastructure management:

| Stage | What It Does |
|-------|-------------|
| **Detect Changes** | Auto-detects which Terraform directories changed |
| **Validate** | Format check, `terraform validate`, TFLint across changed directories |
| **Security** | Static analysis with tfsec and Checkov |
| **Plan** | Generates plan, posts output as PR comment for review |
| **Apply** | Auto-applies on merge to `main` with manual environment approval |

**Trigger:** Runs only when files under `terraform/` change.

### Infrastructure (Terraform)

Production-ready AWS infrastructure:

- **VPC** — Multi-AZ (3 AZs), public/private subnets, NAT gateways
- **EKS** — Managed Kubernetes cluster with IRSA, managed node groups, core add-ons
- **ECR** — Container registry with immutable tags, scan-on-push, lifecycle policy
- **RDS PostgreSQL** — Multi-AZ, encrypted, performance insights, 14-day backups
- **ElastiCache Redis** — Multi-node replication group, encryption at rest and in transit, auto-failover

### Kubernetes Manifests

- **Deployment** — 3 replicas, rolling update, topology spread across AZs
- **Service** — ClusterIP service
- **HPA** — Auto-scaling based on CPU (70%) and memory (80%) with scale-up/down policies
- **Security** — Non-root container, read-only filesystem, dropped capabilities, secret references

### Dockerfile

Multi-stage build with:
- Non-root user
- Health check
- Gunicorn production server

## How to Use

### Prerequisites

- AWS account with IAM OIDC provider configured for GitHub Actions
- GitHub repository with the following secrets configured:

| Secret | Description |
|--------|-------------|
| `AWS_OIDC_ROLE` | IAM role ARN for GitHub Actions (staging) |
| `AWS_PROD_OIDC_ROLE` | IAM role ARN for GitHub Actions (production) |
| `SLACK_WEBHOOK` | Slack incoming webhook URL for notifications |

- GitHub environments created: `staging` and `production` (with required reviewers on production)

### Step 1: Set Up Infrastructure

```bash
cd terraform/

# Initialize Terraform (update backend config in main.tf first)
terraform init

# Review the plan
terraform plan

# Apply
terraform apply
```

### Step 2: Push Application Code

```bash
# Create a feature branch
git checkout -b feature/my-change

# Make changes, commit, push
git add .
git commit -m "feat: add new feature"
git push origin feature/my-change

# Open a pull request — CI pipeline runs automatically
# On merge to main — build, push, and deploy kicks in
```

### Step 3: Infrastructure Changes

```bash
# Modify any file under terraform/
# Open a PR — plan is generated and posted as a comment
# On merge — changes are applied automatically
```

### Pipeline Flow

```
Pull Request Opened
    │
    ├── Lint & Format
    ├── Unit & Integration Tests (PostgreSQL + Redis)
    └── Security Scan (Trivy)
         │
         ▼ (all pass)
Merge to main
    │
    ▼
Build Docker Image → Push to ECR → Scan Image
    │
    ▼
Deploy to Staging (canary 30%) → Smoke Tests → Promote
    │
    ▼
Deploy to Production (canary 20%) → Smoke Tests → Promote
    │
    ▼
Slack Notification
```

## Customization

1. **Change application type** — Replace Python/Ruff/pytest steps in `ci.yml` with your stack (Node, Go, Java, etc.)
2. **Change cloud provider** — Replace AWS-specific steps and Terraform modules with your provider
3. **Add environments** — Duplicate the staging deploy job for additional environments (dev, QA)
4. **Adjust scaling** — Modify HPA thresholds and replica counts in `k8s/production/deployment.yaml`
5. **Add monitoring** — Integrate Prometheus/Grafana by adding ServiceMonitor and dashboard resources

## Tech Stack

- **CI/CD:** GitHub Actions
- **Infrastructure:** Terraform, AWS (EKS, VPC, ECR, RDS, ElastiCache)
- **Containers:** Docker, Kubernetes
- **Security:** Trivy, tfsec, Checkov
- **Deployment Strategy:** Canary with automatic promotion
- **Notifications:** Slack

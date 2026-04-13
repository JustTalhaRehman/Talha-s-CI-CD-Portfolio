# CI/CD Pipeline

End-to-end CI/CD pipeline with GitHub Actions, Terraform, Kubernetes, and AWS. The app is a simple FastAPI service — the focus is the pipeline and infrastructure around it.

## What's in here

**App** (`app/`) — FastAPI service with `/health`, `/ready`, `/metrics`, and `/users` endpoints. Uses PostgreSQL and Redis.

**CI/CD** (`.github/workflows/ci.yml`) — Runs on every PR and merge to `main`:

| Stage | What it does |
|-------|-------------|
| Lint & Format | Ruff + Black checks |
| Test | pytest with real Postgres and Redis service containers |
| Security Scan | Trivy filesystem scan, results uploaded to GitHub Security tab |
| Build & Push | Docker image built and pushed to Amazon ECR |
| Deploy | Staging → smoke tests → Production (manual approval gate) |

**Infrastructure Pipeline** (`.github/workflows/iac-pipeline.yml`) — Triggered only when `terraform/` files change. Validates, runs tfsec + Checkov, posts the plan as a PR comment, and applies on merge to `main`.

**Infrastructure** (`terraform/`) — VPC, EKS cluster, ECR, RDS PostgreSQL, ElastiCache Redis.

**Kubernetes** (`k8s/`) — Staging and production manifests with HPA, resource limits, and non-root containers.

## Pipeline Flow

```
Pull Request opened
  ├── Lint & Format
  ├── Tests (Postgres + Redis containers)
  └── Security Scan
          │
          ▼  merge to main
  Build Docker image → push to ECR
          │
          ▼
  Deploy to Staging → smoke tests
          │
          ▼
  Deploy to Production (requires approval) → smoke tests
          │
          ▼
  Slack notification
```

## Setup

See [`setup/aws-setup.md`](setup/aws-setup.md) for the one-time AWS prep — S3/DynamoDB for Terraform state, GitHub OIDC provider, and IAM roles.

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AWS_ACCOUNT_ID` | AWS account ID |
| `AWS_OIDC_ROLE` | IAM role ARN for staging |
| `AWS_PROD_OIDC_ROLE` | IAM role ARN for production |
| `SLACK_WEBHOOK` | Slack incoming webhook URL |

### GitHub Environments

Create two environments in your repo settings:
- `staging` — no restrictions
- `production` — add required reviewers

## Running locally

```bash
# Start the app with Postgres and Redis
docker compose up

# App will be available at http://localhost:8000
```

Or without Docker:

```bash
pip install -r requirements.txt

export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/appdb
export REDIS_URL=redis://localhost:6379/0

pytest           # run tests
uvicorn app.main:app --reload   # start the app
```

## Tech Stack

- **CI/CD:** GitHub Actions
- **Infrastructure:** Terraform, AWS (EKS, ECR, RDS, ElastiCache)
- **Containers:** Docker, Kubernetes
- **Security:** Trivy, tfsec, Checkov
- **App:** Python, FastAPI, PostgreSQL, Redis

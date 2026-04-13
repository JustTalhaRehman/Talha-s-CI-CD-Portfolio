# Complete Architecture Documentation - A to Z

## Overview
Production-grade CI/CD pipeline with Infrastructure as Code using GitHub Actions, Terraform, Kubernetes, and AWS.

---

## 1. DEVELOPMENT FLOW ARCHITECTURE

### 1.1 Code Repository Structure
```
Talha-s-CI-CD-Portfolio/
|
+-- .github/workflows/           # GitHub Actions pipelines
|   +-- ci.yml                   # Application CI/CD pipeline
|   +-- iac-pipeline.yml         # Infrastructure pipeline
|
+-- app/                         # Application code
|   +-- main.py                  # FastAPI application
|   +-- tests/                   # Test suite
|   +-- __init__.py
|
+-- k8s/                         # Kubernetes manifests
|   +-- staging/                 # Staging environment
|   |   +-- namespace.yaml
|   |   +-- deployment.yaml
|   |   +-- serviceaccount.yaml
|   |   +-- secrets.yaml
|   +-- production/              # Production environment
|       +-- namespace.yaml
|       +-- deployment.yaml
|       +-- serviceaccount.yaml
|       +-- secrets.yaml
|
+-- terraform/                   # Infrastructure as Code
|   +-- main.tf                  # Main infrastructure
|   +-- variables.tf             # Input variables
|   +-- outputs.tf               # Output values
|
+-- Dockerfile                   # Container definition
+-- requirements.txt             # Python dependencies
+-- .env.example                 # Environment template
+-- setup/                       # Setup guides
    +-- aws-setup.md
```

---

## 2. CI/CD PIPELINE COMPONENTS (ci.yml)

### 2.1 Trigger Events
```
Pull Request to main:
  - Lint & Format
  - Test (with PostgreSQL + Redis)
  - Security Scan (Trivy)

Push to main:
  - All above stages
  - Build & Push Docker
  - Deploy to Staging
  - Deploy to Production
  - Slack Notifications
```

### 2.2 Detailed Pipeline Stages

#### Stage 1: Lint & Format
- **Tool**: Ruff (Python linting)
- **Tool**: Black (Code formatting)
- **Purpose**: Code quality enforcement
- **Environment**: Ubuntu Latest
- **Python Version**: 3.12

#### Stage 2: Test
- **Framework**: pytest with coverage
- **Database**: PostgreSQL 16 (service container)
- **Cache**: Redis 7 (service container)
- **Coverage**: XML + HTML reports
- **Reporting**: Codecov integration

#### Stage 3: Security Scan
- **Tool**: Trivy filesystem scanner
- **Output**: SARIF format
- **Integration**: GitHub Security tab
- **Scope**: All files in repository

#### Stage 4: Build & Push Docker
- **Registry**: Amazon ECR
- **Build**: Multi-stage Docker build
- **Security**: Image vulnerability scanning
- **Artifacts**: SBOM generation
- **Tags**: Git SHA + latest

#### Stage 5: Deploy Staging
- **Strategy**: Canary deployment (30%)
- **Environment**: Staging
- **Cluster**: EKS (myapp-staging)
- **Validation**: Smoke tests
- **Service**: LoadBalancer type

#### Stage 6: Deploy Production
- **Strategy**: Canary deployment (20%)
- **Environment**: Production (manual approval)
- **Cluster**: EKS (myapp-production)
- **Validation**: Smoke tests
- **Promotion**: Full rollout

#### Stage 7: Notify
- **Channel**: Slack
- **Triggers**: Success/Failure
- **Content**: Deployment status + commit info

---

## 3. INFRASTRUCTURE PIPELINE COMPONENTS (iac-pipeline.yml)

### 3.1 Trigger Events
```
Pull Request (terraform/**):
  - Detect changes
  - Validate Terraform
  - Security scan
  - Generate plan (PR comment)

Push to main (terraform/**):
  - All above stages
  - Apply infrastructure
  - Update outputs
```

### 3.2 Infrastructure Stages

#### Stage 1: Detect Changes
- **Method**: Git diff analysis
- **Scope**: terraform/** directory
- **Logic**: PR vs Push handling
- **Output**: Boolean flag for downstream jobs

#### Stage 2: Validate
- **Tool**: Terraform format check
- **Tool**: Terraform validate
- **Tool**: TFLint (linting)
- **Purpose**: Code quality and syntax

#### Stage 3: Security Scan
- **Tool**: tfsec (Terraform security)
- **Tool**: Checkov (policy compliance)
- **Output**: SARIF format
- **Integration**: GitHub Security tab

#### Stage 4: Plan
- **Action**: terraform plan
- **Output**: Human-readable plan
- **Integration**: PR comment
- **Storage**: Plan artifact (7 days)

#### Stage 5: Apply
- **Condition**: Merge to main only
- **Action**: terraform apply
- **Environment**: Production (manual approval)
- **Output**: Infrastructure updates

---

## 4. AWS INFRASTRUCTURE COMPONENTS

### 4.1 Network Layer (VPC)
```
VPC: 10.0.0.0/16
|
+-- Public Subnets (3 AZs):
|   +-- 10.0.101.0/24 (us-east-2a)
|   +-- 10.0.102.0/24 (us-east-2b)
|   +-- 10.0.103.0/24 (us-east-2c)
|   +-- Tags: kubernetes.io/role/elb=1
|
+-- Private Subnets (3 AZs):
|   +-- 10.0.1.0/24 (us-east-2a)
|   +-- 10.0.2.0/24 (us-east-2b)
|   +-- 10.0.3.0/24 (us-east-2c)
|   +-- Tags: kubernetes.io/role/internal-elb=1
|
+-- NAT Gateways (3) - One per AZ
+-- Internet Gateway (1)
+-- Route Tables (Public + Private)
```

### 4.2 Container Registry (ECR)
```
Repository: myapp
|
+-- Configuration:
|   +-- Image Tag Mutability: IMMUTABLE
|   +-- Scan on Push: Enabled
|   +-- Encryption: KMS
|
+-- Lifecycle Policy:
|   +-- Keep last 20 images
|   +-- Expire older images
|
+-- Images:
|   +-- latest (production)
|   +-- <git-sha> (specific versions)
```

### 4.3 Kubernetes Cluster (EKS)
```
Cluster: myapp-production
|
+-- Configuration:
|   +-- Version: 1.31
|   +-- Endpoint: Public access
|   +-- IRSA: Enabled
|
+-- Node Groups:
|   +-- Instance Type: m6i.large
|   +-- Min: 2, Desired: 3, Max: 6
|   +-- Labels: workload=general
|
+-- Add-ons:
|   +-- CoreDNS
|   +-- kube-proxy
|   +-- VPC CNI
```

### 4.4 Database Layer (RDS PostgreSQL)
```
Instance: myapp-production
|
+-- Configuration:
|   +-- Engine: PostgreSQL 16.4
|   +-- Instance Class: db.r6g.large
|   +-- Storage: 50GB (max 200GB)
|   +-- Multi-AZ: Enabled
|
+-- Security:
|   +-- Encryption: At rest + in transit
|   +-- Backup: 14 days retention
|   +-- Performance Insights: Enabled
|
+-- Network:
|   +-- Subnet: Private
|   +-- Security Group: EKS nodes only
```

### 4.5 Cache Layer (ElastiCache Redis)
```
Cluster: myapp-production
|
+-- Configuration:
|   +-- Engine: Redis 7.1
|   +-- Node Type: cache.r6g.large
|   +-- Nodes: 2 (replication)
|
+-- Security:
|   +-- Encryption: At rest + in transit
|   +-- Auto-failover: Enabled
|   +-- Snapshot: 7 days retention
|
+-- Network:
|   +-- Subnet: Private
|   +-- Security Group: EKS nodes only
```

---

## 5. KUBERNETES APPLICATION ARCHITECTURE

### 5.1 Production Environment
```
Namespace: production
|
+-- ServiceAccount: myapp
|   +-- IAM Role: IRSA mapped
|
+-- Secrets: myapp-secrets
|   +-- database-url (base64)
|   +-- redis-url (base64)
|
+-- Deployment: myapp
|   +-- Replicas: 3
|   +-- Strategy: RollingUpdate
|   +-- Image: ECR repository
|   +-- Resources: 100m-500m CPU, 256Mi-512Mi RAM
|
+-- Service: myapp
|   +-- Type: ClusterIP
|   +-- Port: 80 -> 8000
|
+-- HPA: myapp
|   +-- Min: 3, Max: 10 replicas
|   +-- Metrics: CPU 70%, Memory 80%
|   +-- Scale policies: Up 2/min, Down 1/2min
```

### 5.2 Staging Environment
```
Namespace: staging
|
+-- ServiceAccount: myapp
+-- Secrets: myapp-secrets
+-- Deployment: myapp
|   +-- Replicas: 2
|   +-- Resources: 50m-200m CPU, 128Mi-256Mi RAM
|
+-- Service: myapp
|   +-- Type: LoadBalancer (external access)
```

---

## 6. SECURITY ARCHITECTURE

### 6.1 Authentication & Authorization
```
GitHub Actions
|
+-- OIDC Authentication
|   +-- Provider: token.actions.githubusercontent.com
|   +-- Trust: GitHub repository
|
+-- IAM Roles:
|   +-- Staging: PowerUserAccess + ECR
|   +-- Production: ECR + EKS permissions
|
+-- IRSA (IAM Roles for Service Accounts)
|   +-- Kubernetes ServiceAccount -> IAM Role mapping
|   +-- Pod-level AWS permissions
```

### 6.2 Network Security
```
VPC Security
|
+-- Public Subnets:
|   +-- Load Balancers
|   +-- NAT Gateways
|
+-- Private Subnets:
|   +-- EKS Nodes
|   +-- RDS Database
|   +-- ElastiCache Redis
|
+-- Security Groups:
|   +-- EKS Node SG
|   +-- RDS SG (EKS only)
|   +-- Redis SG (EKS only)
```

### 6.3 Container Security
```
Docker & Kubernetes
|
+-- Container Hardening:
|   +-- Non-root user
|   +-- Read-only filesystem
|   +-- Dropped capabilities
|   +-- Health checks
|
+-- Image Security:
|   +-- Trivy scanning
|   +-- ECR scan on push
|   +-- SBOM generation
|
+-- Runtime Security:
|   +-- Pod Security Policies
|   +-- Network policies (if needed)
```

---

## 7. DATA FLOW ARCHITECTURE

### 7.1 Application Request Flow
```
User Request
|
+-- Load Balancer (ALB)
|   +-- SSL termination
|   +-- Health checks
|
+-- Kubernetes Service
|   +-- ClusterIP routing
|   +-- Service discovery
|
+-- Pod (Application)
|   +-- FastAPI application
|   +-- Request processing
|
+-- Database Layer
|   +-- PostgreSQL (persistent data)
|   +-- Redis (caching/sessions)
|
+-- Response Path (reverse order)
```

### 7.2 CI/CD Pipeline Flow
```
Developer Push
|
+-- GitHub Actions Trigger
|   +-- Code analysis
|   +-- Security scanning
|   +-- Testing
|
+-- Docker Build
|   +-- Multi-stage build
|   +-- Security scanning
|   +-- ECR push
|
+-- Kubernetes Deployment
|   +-- Image update
|   +-- Rolling update
|   +-- Health validation
|
+-- Monitoring & Alerting
|   +-- Health checks
|   +-- Slack notifications
```

---

## 8. MONITORING & OBSERVABILITY

### 8.1 Health Checks
```
Application Health
|
+-- Liveness Probe:
|   +-- Path: /health
|   +-- Interval: 15s
|   +-- Timeout: 3s
|   +-- Failure threshold: 3
|
+-- Readiness Probe:
|   +-- Path: /ready
|   +-- Interval: 10s
|   +-- Timeout: 3s
|   +-- Database + Redis connectivity
|
+-- Startup Probe:
|   +-- Initial delay: 10s
|   +-- Path: /health
```

### 8.2 Application Metrics
```
Custom Endpoints
|
+-- /metrics:
|   +-- Visit counter (Redis)
|   +-- Status: ok/error
|
+-- /health:
|   +-- Application status
|   +-- Version info
|
+-- /ready:
|   +-- Database connection status
|   +-- Redis connection status
```

---

## 9. CONFIGURATION MANAGEMENT

### 9.1 Environment Variables
```
Application Config
|
+-- Database:
|   +-- DATABASE_URL (from Secrets)
|
+-- Cache:
|   +-- REDIS_URL (from Secrets)
|
+-- Application:
|   +-- Environment (staging/production)
|   +-- Log level
|   +-- Debug settings
```

### 9.2 Kubernetes Configuration
```
Manifest Management
|
+-- Namespaces:
|   +-- Environment isolation
|   +-- Resource quotas
|
+-- Secrets:
|   +-- Base64 encoded
|   +-- External secrets management
|
+-- ConfigMaps:
|   +-- Application configuration
|   +-- Feature flags
```

---

## 10. DISASTER RECOVERY & BACKUP

### 10.1 Data Backup Strategy
```
Database Backup
|
+-- RDS Automated Backups:
|   +-- Retention: 14 days
|   +-- Point-in-time recovery
|   +-- Cross-region backup (optional)
|
+-- Redis Snapshots:
|   +-- Retention: 7 days
|   +-- Automatic backup
|
+-- Application State:
|   +-- Stateless design
|   +-- External session storage
```

### 10.2 Infrastructure Recovery
```
Terraform State
|
+-- S3 Backend:
|   +-- Versioning enabled
|   +-- Encryption at rest
|   +-- Cross-region replication
|
+-- State Locking:
|   +-- DynamoDB table
|   +-- Consistent state management
|
+-- Recovery Process:
|   +-- terraform import
|   +-- State restoration
```

---

## 11. PERFORMANCE OPTIMIZATION

### 11.1 Application Performance
```
FastAPI Optimization
|
+-- Async/await patterns
+-- Connection pooling
+-- Redis caching
+-- Gunicorn workers (4)
+-- Gunicorn threads (2)
```

### 11.2 Infrastructure Performance
```
AWS Optimization
|
+-- EKS Node Groups:
|   +-- Auto Scaling
|   +-- Spot instances (optional)
|   +-- Instance right-sizing
|
+-- Database:
|   +-- Connection pooling
|   +-- Performance Insights
|   +-- Read replicas (optional)
|
+-- Caching:
|   +-- Redis cluster
|   +-- Application caching
|   +-- CDN integration (optional)
```

---

## 12. COST OPTIMIZATION

### 12.1 Resource Efficiency
```
Cost Management
|
+-- EKS:
|   +-- Right-sized instances
|   +-- Auto scaling
|   +-- Spot instances
|
+-- RDS:
|   +-- Reserved instances
|   +-- Storage optimization
|   +-- Backup retention
|
+-- ECR:
|   +-- Lifecycle policies
|   +-- Image optimization
|   +-- Storage classes
```

---

## 13. COMPLIANCE & GOVERNANCE

### 13.1 Security Compliance
```
Compliance Framework
|
+-- Security Scanning:
|   +-- Trivy (containers)
|   +-- tfsec (infrastructure)
|   +-- Checkov (policies)
|
+-- Access Control:
|   +-- IAM least privilege
|   +-- GitHub environment protection
|   +-- Manual approvals
|
+-- Audit Trail:
|   +-- CloudTrail logging
|   +-- GitHub audit log
|   +-- Terraform state history
```

---

## 14. COMPLETE TECHNOLOGY STACK

### 14.1 Development Tools
- **Language**: Python 3.12
- **Framework**: FastAPI
- **Testing**: pytest
- **Linting**: Ruff, Black
- **Containerization**: Docker

### 14.2 CI/CD Platform
- **Pipeline**: GitHub Actions
- **Registry**: Amazon ECR
- **Scanning**: Trivy, tfsec, Checkov
- **Notifications**: Slack

### 14.3 Infrastructure
- **IaC**: Terraform
- **Cloud**: AWS
- **Orchestration**: Kubernetes (EKS)
- **Database**: PostgreSQL (RDS)
- **Cache**: Redis (ElastiCache)

### 14.4 Networking
- **VPC**: AWS VPC
- **Load Balancing**: Application Load Balancer
- **DNS**: Route 53 (optional)
- **CDN**: CloudFront (optional)

### 14.5 Monitoring
- **Health Checks**: Kubernetes probes
- **Metrics**: Custom endpoints
- **Logging**: CloudWatch (optional)
- **Alerting**: Slack

---

## 15. DEPLOYMENT STRATEGIES

### 15.1 Canary Deployment
```
Canary Process
|
+-- Staging Canary (30%):
|   +-- Deploy new version
|   +-- Monitor health
|   +-- Run smoke tests
|
+-- Production Canary (20%):
|   +-- Gradual traffic shift
|   +-- Monitor metrics
|   +-- Full promotion
|
+-- Rollback Strategy:
|   +-- Automatic on failure
|   +-- Manual trigger
|   +-- Previous version restore
```

---

This architecture provides a complete, production-ready system with every component documented from A to Z. Use this as your reference for creating detailed architecture diagrams.

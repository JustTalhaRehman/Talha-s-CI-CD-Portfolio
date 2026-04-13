# Architecture Diagram Components - Visual Reference

## COLOR CODING FOR DIAGRAMS

### Primary Colors
- **Blue (#2563EB)**: Application Components
- **Green (#16A34A)**: Infrastructure Components  
- **Orange (#EA580C)**: CI/CD Pipeline
- **Purple (#9333EA)**: Security Components
- **Red (#DC2626)**: Data/Storage
- **Gray (#6B7280)**: Network/Connectivity

---

## 1. DEVELOPER WORKFLOW COMPONENTS

### Developer Machine
```
[Developer]
  - Git Client
  - IDE/Editor
  - Local Testing
```

### GitHub Repository
```
[GitHub Repo]
  - Main Branch
  - Feature Branches
  - Pull Requests
  - Issues/Projects
```

---

## 2. CI/CD PIPELINE VISUAL COMPONENTS

### GitHub Actions Runner
```
[GitHub Actions]
  |
  +-- [Lint & Format]
  |     +-- Ruff Icon
  |     +-- Black Icon
  |
  +-- [Test]
  |     +-- pytest Icon
  |     +-- PostgreSQL Logo
  |     +-- Redis Logo
  |
  +-- [Security Scan]
  |     +-- Trivy Shield Icon
  |     +-- SARIF Format Icon
  |
  +-- [Build & Push]
  |     +-- Docker Whale Logo
  |     +-- ECR Logo
  |     +-- SBOM Icon
  |
  +-- [Deploy Staging]
  |     +-- 30% Badge
  |     +-- EKS Logo
  |     +-- Smoke Test Icon
  |
  +-- [Deploy Production]
  |     +-- 20% Badge
  |     +-- EKS Logo
  |     +-- Manual Approval Icon
  |
  +-- [Notify]
        +-- Slack Logo
```

---

## 3. AWS INFRASTRUCTURE VISUAL COMPONENTS

### Network Layer
```
[VPC - 10.0.0.0/16]
  |
  +-- [Public Subnets]
  |     +-- [Internet Gateway]
  |     +-- [NAT Gateways x3]
  |     +-- [ALB/Load Balancer]
  |
  +-- [Private Subnets]
        +-- [EKS Nodes]
        +-- [RDS PostgreSQL]
        +-- [ElastiCache Redis]
```

### EKS Cluster
```
[EKS Cluster - myapp-production]
  |
  +-- [Control Plane]
  |     +-- API Server
  |     +-- etcd
  |     +-- Scheduler
  |     +-- Controller Manager
  |
  +-- [Node Group]
  |     +-- [Worker Nodes x3]
  |     +-- [Instance: m6i.large]
  |     +-- [Kubelet]
  |     +-- [kube-proxy]
  |
  +-- [Add-ons]
        +-- [CoreDNS]
        +-- [VPC CNI]
        +-- [kube-proxy]
```

### Storage Components
```
[ECR Repository]
  |
  +-- [Images]
  |     +-- latest
  |     +-- <git-sha>
  |     +-- <version-tags>
  |
  +-- [Security]
  |     +-- Scan on Push
  |     +-- Vulnerability Reports
  |
  +-- [Lifecycle]
        +-- Keep 20 images
        +-- Auto-expire

[RDS PostgreSQL]
  |
  +-- [Primary Instance]
  |     +-- db.r6g.large
  |     +-- Multi-AZ
  |     +-- Encrypted
  |
  +-- [Backup]
  |     +-- 14 days retention
  |     +-- Point-in-time recovery
  |
  +-- [Monitoring]
        +-- Performance Insights
        +-- Enhanced Monitoring

[ElastiCache Redis]
  |
  +-- [Primary Node]
  |     +-- cache.r6g.large
  |     +-- Encrypted
  |
  +-- [Replica Node]
  |     +-- Auto-failover
  |     +-- Read replicas
  |
  +-- [Backup]
        +-- 7 days snapshots
```

---

## 4. KUBERNETES APPLICATION COMPONENTS

### Production Namespace
```
[Production Namespace]
  |
  +-- [ServiceAccount: myapp]
  |     +-- [IAM Role Mapping]
  |
  +-- [Secret: myapp-secrets]
  |     +-- database-url
  |     +-- redis-url
  |
  +-- [Deployment: myapp]
  |     +-- [Replicas: 3]
  |     +-- [Container: FastAPI]
  |     +-- [Resources: CPU/Memory]
  |     +-- [Health Probes]
  |
  +-- [Service: myapp]
  |     +-- [ClusterIP]
  |     +-- [Port: 80->8000]
  |
  +-- [HPA: myapp]
        +-- [Min: 3, Max: 10]
        +-- [CPU: 70%]
        +-- [Memory: 80%]
```

### Staging Namespace
```
[Staging Namespace]
  |
  +-- [ServiceAccount: myapp]
  +-- [Secret: myapp-secrets]
  +-- [Deployment: myapp]
  |     +-- [Replicas: 2]
  |     +-- [Resources: Smaller]
  |
  +-- [Service: myapp]
        +-- [LoadBalancer]
        +-- [External Access]
```

---

## 5. SECURITY ARCHITECTURE COMPONENTS

### Authentication Flow
```
[GitHub Actions]
  |
  +-- [OIDC Provider]
  |     +-- token.actions.githubusercontent.com
  |
  +-- [IAM Role: Staging]
  |     +-- [PowerUserAccess]
  |     +-- [ECR Permissions]
  |
  +-- [IAM Role: Production]
        +-- [ECR Permissions]
        +-- [EKS Permissions]
```

### IRSA Mapping
```
[Kubernetes ServiceAccount]
  |
  +-- [IAM Role]
  |     +-- [Pod Identity]
  |     +-- [AWS Permissions]
  |
  +-- [Pod]
        +-- [AWS SDK Access]
        +-- [No Access Keys]
```

### Security Scanning
```
[Security Tools]
  |
  +-- [Trivy]
  |     +-- [Container Scanning]
  |     +-- [Filesystem Scanning]
  |
  +-- [tfsec]
  |     +-- [Terraform Security]
  |     +-- [AWS Best Practices]
  |
  +-- [Checkov]
  |     +-- [Policy Compliance]
  |     +-- [Industry Standards]
  |
  +-- [GitHub Security]
        +-- [SARIF Integration]
        +-- [Vulnerability Alerts]
```

---

## 6. DATA FLOW COMPONENTS

### Request Flow
```
[User]
  |
  +-- [DNS] (Route 53)
  |
  +-- [ALB/Load Balancer]
  |     +-- [SSL Termination]
  |     +-- [Health Checks]
  |
  +-- [Kubernetes Service]
  |     +-- [ClusterIP]
  |     +-- [Service Discovery]
  |
  +-- [Pod]
  |     +-- [FastAPI App]
  |     +-- [Request Processing]
  |
  +-- [Database Layer]
  |     +-- [PostgreSQL]
  |     +-- [Redis Cache]
  |
  +-- [Response]
        +-- [Reverse Path]
```

### CI/CD Flow
```
[Developer Push]
  |
  +-- [GitHub Webhook]
  |
  +-- [Actions Trigger]
  |     +-- [Code Analysis]
  |     +-- [Security Scan]
  |     +-- [Testing]
  |
  +-- [Docker Build]
  |     +-- [Multi-stage]
  |     +-- [Security Scan]
  |     +-- [ECR Push]
  |
  +-- [Kubernetes Deploy]
  |     +-- [Image Update]
  |     +-- [Rolling Update]
  |     +-- [Health Validation]
  |
  +-- [Monitoring]
        +-- [Slack Notify]
        +-- [Health Checks]
```

---

## 7. MONITORING COMPONENTS

### Health Check System
```
[Application Health]
  |
  +-- [Liveness Probe]
  |     +-- [Path: /health]
  |     +-- [Interval: 15s]
  |     +-- [Failure: 3x]
  |
  +-- [Readiness Probe]
  |     +-- [Path: /ready]
  |     +-- [Interval: 10s]
  |     +-- [DB + Redis Check]
  |
  +-- [Startup Probe]
        +-- [Initial Delay: 10s]
        +-- [Path: /health]
```

### Metrics Collection
```
[Custom Metrics]
  |
  +-- [/metrics Endpoint]
  |     +-- [Visit Counter]
  |     +-- [Response Times]
  |     +-- [Error Rates]
  |
  +-- [/health Endpoint]
  |     +-- [App Status]
  |     +-- [Version Info]
  |
  +-- [/ready Endpoint]
        +-- [DB Status]
        +-- [Redis Status]
```

---

## 8. INFRASTRUCTURE AS CODE COMPONENTS

### Terraform Components
```
[Terraform]
  |
  +-- [State Management]
  |     +-- [S3 Bucket]
  |     +-- [DynamoDB Lock]
  |     +-- [State Versioning]
  |
  +-- [Modules]
  |     +-- [EKS Module]
  |     +-- [VPC Module]
  |     +-- [RDS Module]
  |
  +-- [Validation]
        +-- [Format Check]
        +-- [Validate]
        +-- [TFLint]
```

### GitOps Flow
```
[Terraform Code]
  |
  +-- [PR Trigger]
  |     +-- [Plan Generation]
  |     +-- [Security Scan]
  |     +-- [PR Comment]
  |
  +-- [Merge Trigger]
  |     +-- [Apply Changes]
  |     +-- [Update Outputs]
  |
  +-- [State Management]
        +-- [Remote State]
        +-- [Locking]
        +-- [Versioning]
```

---

## 9. ICON LIBRARY FOR DIAGRAMS

### Technology Icons
```
GitHub:     [GitHub Logo]
Docker:     [Docker Whale]
AWS:        [AWS Cloud Logo]
Kubernetes: [K8S Helm Wheel]
PostgreSQL: [PostgreSQL Elephant]
Redis:      [Redis Stack]
FastAPI:    [FastAPI Lightning]
Python:     [Python Logo]
Slack:      [Slack Logo]
Terraform:  [Terraform Logo]
Trivy:      [Trivy Shield]
```

### Status Icons
```
Success:    [Green Checkmark]
Warning:    [Yellow Warning]
Error:      [Red X]
Processing: [Blue Spinner]
Pending:    [Gray Clock]
```

### Flow Icons
```
Arrow:      [Right Arrow]
Bidirectional: [Double Arrow]
Cloud:      [Cloud Icon]
Database:   [Database Cylinder]
Server:     [Server Rack]
Lock:       [Lock Icon]
Key:        [Key Icon]
Shield:     [Shield Icon]
```

---

## 10. LAYER ARCHITECTURE VISUALIZATION

### Layer 1: Foundation
```
[AWS Cloud Foundation]
  |
  +-- [VPC/Networking]
  +-- [IAM/Roles]
  +-- [Security Groups]
```

### Layer 2: Infrastructure
```
[Infrastructure Layer]
  |
  +-- [EKS Cluster]
  +-- [RDS Database]
  +-- [ElastiCache Redis]
  +-- [ECR Registry]
```

### Layer 3: Platform
```
[Platform Layer]
  |
  +-- [Kubernetes Resources]
  +-- [Service Mesh (optional)]
  +-- [Ingress Controller]
  +-- [Monitoring Stack]
```

### Layer 4: Application
```
[Application Layer]
  |
  +-- [FastAPI Application]
  +-- [Microservices]
  +-- [API Gateway]
  +-- [Load Balancer]
```

### Layer 5: CI/CD
```
[CI/CD Layer]
  |
  +-- [GitHub Actions]
  +-- [Pipeline Stages]
  +-- [Security Scanning]
  +-- [Deployment Automation]
```

---

Use these components as building blocks for your architecture diagrams. Each component can be combined with others to create comprehensive visual representations of your entire system architecture.

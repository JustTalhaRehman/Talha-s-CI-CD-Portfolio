# Flow Diagrams

Visual step-by-step diagrams for every process in the CI/CD pipeline and infrastructure.

---

## 1. End-to-End Development Flow

```mermaid
flowchart TD
    A[Developer Machine] -->|git push| B[GitHub Repository]
    B -->|webhook trigger| C[GitHub Actions CI Pipeline]
    C --> D[Lint & Format]
    C --> E[Test Suite]
    C --> F[Security Scan]
    D & E & F -->|all pass| G[Docker Build]
    G -->|docker push| H[Amazon ECR]
    H -->|image scan| I[Security Validation]
    I -->|deploy trigger| J[Kubernetes Deployment]
    J -->|health check| K[Running Application]
    K -->|notification| L[Slack Alert]
```

---

## 2. Infrastructure Provisioning Flow

```mermaid
flowchart TD
    A[Terraform Code Change] -->|git push| B[GitHub Actions IaC Pipeline]
    B --> C{Detect Terraform Changes}
    C -->|no changes| Z[Skip]
    C -->|changes detected| D[Terraform Validation]
    D --> D1[Format Check]
    D --> D2[Validate]
    D --> D3[TFLint]
    D1 & D2 & D3 -->|all pass| E[Security Scanning]
    E --> E1[tfsec]
    E --> E2[Checkov]
    E --> E3[SARIF Upload]
    E1 & E2 & E3 -->|security pass| F[Terraform Plan]
    F --> G[PR Comment]
    F --> H[Plan Artifact]
    G -->|merged to main| I[Terraform Apply]
    I -->|create/update resources| J[AWS Infrastructure]
    J --> K[Infrastructure Ready]
```

---

## 3. Application Request Flow

```mermaid
flowchart TD
    A[End User] -->|HTTPS Request| B[DNS Resolution / Route 53]
    B --> C[Application Load Balancer]
    C -->|SSL Termination + Health Check| D[Kubernetes Service]
    D -->|ClusterIP Routing| E[Kubernetes Pod / FastAPI]
    E --> F{Business Logic}
    F --> G[Database Query]
    F --> H[Cache Check]
    G --> I[(PostgreSQL)]
    H --> J[(Redis)]
    I & J -->|aggregate response| K[HTTP Response]
    K --> A
```

---

## 4. Security Authentication Flow

```mermaid
flowchart TD
    A[GitHub Actions Runner] -->|request credentials| B[GitHub OIDC Provider]
    B -->|token.actions.githubusercontent.com| C[AWS STS]
    C -->|assume role with web identity| D[IAM Role]
    D -->|temporary credentials| E[AWS Services]
    E --> F[ECR Access]
    E --> G[EKS Access]
    E --> H[S3 Access]
    F & G & H -->|operations complete| I[Task Execution]
```

---

## 5. Kubernetes Deployment Flow

```mermaid
flowchart TD
    A[CI Pipeline] -->|deployment trigger| B[Image Update]
    B -->|kubectl set image| C[Deployment Controller]
    C -->|rolling update strategy| D[New ReplicaSet]
    D -->|create new pods| E[Pod Creation]
    E -->|pull image + start container| F[Health Checks]
    F --> F1[Liveness Probe]
    F --> F2[Readiness Probe]
    F --> F3[Startup Probe]
    F1 & F2 & F3 -->|pods healthy| G[Service Update]
    G -->|route traffic| H[Old Pod Termination]
    H -->|graceful shutdown| I[Deployment Complete]
```

---

## 6. Canary Deployment Flow

```mermaid
flowchart TD
    A[Current Version - 100% traffic] -->|start canary| B[Canary Deployment - 20% traffic]
    B -->|monitor metrics| C{Health Monitoring}
    C --> C1[Error Rate]
    C --> C2[Response Time]
    C --> C3[CPU / Memory]
    C1 & C2 & C3 -->|healthy| D[Traffic Shift 50%]
    D -->|gradual promotion| E[Full Deployment 100%]
    E -->|terminate old version| F[Deployment Complete]
    C1 & C2 & C3 -->|unhealthy| G[Rollback]
    G --> A
```

---

## 7. Data Persistence Flow

```mermaid
flowchart TD
    A[Application Pod] -->|database connection| B[Connection Pool]
    B -->|get connection| C[(PostgreSQL RDS)]
    C --> D[Primary Instance]
    C --> E[Read Replica]
    C --> F[Automated Backup]
    D -->|write| G[Data Storage]
    E -->|read| H[Query Results]
    F -->|snapshot| I[Point-in-Time Recovery]
    G & H -->|return result| J[Application Response]
```

---

## 8. Caching Flow

```mermaid
flowchart TD
    A[Application Request] -->|check cache first| B{Redis Cache}
    B -->|Cache Hit| C[Return Cached Data]
    B -->|Cache Miss| D[(PostgreSQL)]
    B -->|Error| E[Fallback / Direct DB]
    D -->|query result| F[Update Cache]
    F --> G[Response to User]
    C --> G
    E --> G
```

---

## 9. Monitoring & Alerting Flow

```mermaid
flowchart TD
    A[Application] --> B[/health endpoint]
    A --> C[/ready endpoint]
    A --> D[/metrics endpoint]
    B -->|Liveness| E[Kubernetes Probes]
    C -->|Readiness| E
    D -->|Custom Metrics| F[Metrics Server]
    E & F --> G[HPA Controller]
    G -->|scale decision| H[Pod Scaling]
    H -->|notification| I[Slack Alert]
```

---

## 10. Error Handling Flow

```mermaid
flowchart TD
    A[Application Error] -->|error detection| B{Error Classification}
    B --> C[Network Error]
    B --> D[Database Error]
    B --> E[Logic Error]
    B --> F[Infrastructure Error]
    C -->|Retry| C1[Recovery]
    D -->|Reconnect| D1[Recovery]
    E -->|Fallback| E1[Graceful Degradation]
    F -->|Circuit Breaker| F1[Failover]
    C1 & D1 & E1 & F1 -->|if all fail| G[Error Response]
    G -->|log error| H[Monitoring System]
    H -->|alert team| I[Slack Notification]
```

---

## 11. Backup & Recovery Flow

```mermaid
flowchart TD
    A[Automated Backup Scheduler] --> B[RDS Backup]
    B --> C[Daily Snapshot → S3]
    B --> D[Transaction Log → WAL Storage]
    B --> E[Cross-Region → DR Region]
    C & D & E -->|backup complete| F[Backup Verification]

    G[Disaster Event] -->|initiate recovery| H[Point-in-Time Recovery]
    H -->|select backup time| I[Restore from Backup]
    I -->|create new instance| J[Data Validation]
    J -->|verify integrity| K[DNS Update]
    K -->|point to new instance| L[Service Restoration]
```

---

## 12. Cost Optimization Flow

```mermaid
flowchart TD
    A[Resource Monitoring] -->|collect usage data| B[Cost Analysis]
    B --> C[Compute]
    B --> D[Storage]
    B --> E[Network]
    C -->|Right-sizing| C1[Auto Scaling]
    D -->|Lifecycle Policies| D1[Tiered Storage]
    E -->|Reduce Transfer| E1[CDN Usage]
    C1 & D1 & E1 -->|optimization plan| F[Implementation]
    F -->|monitor savings| G[Cost Reduction]
```

---

## 13. Compliance & Audit Flow

```mermaid
flowchart TD
    A[Compliance Check] -->|run security scans| B[Security Tools]
    B --> C[Trivy]
    B --> D[tfsec]
    B --> E[Checkov]
    C -->|Container Scan| F[SARIF Report]
    D -->|IaC Security| F
    E -->|Policy Check| F
    F -->|upload to GitHub| G[Security Tab]
    G -->|review findings| H[Remediation]
    H -->|fix & re-scan| A
```

---

## 14. Feature Deployment Flow

```mermaid
flowchart TD
    A[Feature Development] -->|create branch| B[Feature Branch]
    B -->|push changes| C[Pull Request]
    C -->|trigger CI| D[Automated Testing]
    D --> D1[Unit Tests]
    D --> D2[Integration Tests]
    D --> D3[Security Scan]
    D1 & D2 & D3 -->|all pass| E[Code Review]
    E -->|approve PR| F[Merge to Main]
    F -->|trigger deployment| G[Staging Deployment]
    G -->|smoke tests pass| H[Production Deployment]
    H -->|monitor performance| I[Feature Live]
```

---

## 15. Troubleshooting Flow

```mermaid
flowchart TD
    A[Issue Detection / Alert] --> B{Initial Assessment}
    B --> C[Logs]
    B --> D[Metrics]
    B --> E[Health Endpoints]
    B --> F[K8s Events]
    C --> C1[Log Analysis]
    D --> D1[Performance Review]
    E --> E1[Status Check]
    F --> F1[Event Timeline]
    C1 & D1 & E1 & F1 -->|identify root cause| G[Root Cause Analysis]
    G -->|determine fix| H[Solution Implementation]
    H -->|apply fix| I[Validation]
    I -->|verified| J[Service Restoration]
    J -->|document| K[Post-Mortem]
```

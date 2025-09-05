### E-Commerce Microservices on AWS (Flask, Next.js)

A production-like, minimal e-commerce application to practice key AWS services using a microservices architecture. The system is intentionally small but follows real-world patterns: stateless services, async messaging, CI/CD, observability, and secure-by-default.

#### Services
- Authentication Service
- Cart Service
- Catalog Service
- Inventory Service
- Order Service
- Payment Service
- Notification Service (includes a worker for async processing)

#### Tech Stack
- Frontend: React/Next.js (scaffold to be added)
- Backend: Python 3.12, Flask, Gunicorn
- Messaging/Events: AWS SNS/SQS (LocalStack in local dev)
- Data: Postgres (shared for dev), Redis (cache/session)
- Observability: OpenTelemetry Collector, Jaeger UI
- Infra: Docker Compose (local), Terraform (AWS skeleton)
- CI/CD: GitHub Actions (skeleton)

#### Local Development
Prerequisites: Docker, Docker Compose

1) Copy environment template and adjust if needed
```bash
cp .env.example .env
```

2) Start the stack
```bash
docker compose up -d --build
```

3) Access endpoints
- Auth: http://localhost:8001/healthz
- Cart: http://localhost:8002/healthz
- Catalog: http://localhost:8003/healthz
- Inventory: http://localhost:8004/healthz
- Order: http://localhost:8005/healthz
- Payment: http://localhost:8006/healthz
- Notification: http://localhost:8007/healthz
- Jaeger UI: http://localhost:16686
- LocalStack: http://localhost:4566

LocalStack will auto-create a demo SNS topic and SQS queue and wire them together via init scripts.

#### Repository Layout
```
frontend/                     # Next.js app (scaffold TBD)
infra/
  localstack/
    init-aws.sh               # Creates SNS/SQS resources for local dev
  otel/
    otel-collector-config.yaml
  terraform/                  # AWS infra skeleton (VPC, ECS, ECR, RDS, SQS/SNS)
libs/
  python-common/              # Shared Python lib: logging, tracing, auth, aws, events
services/
  auth-service/
  cart-service/
  catalog-service/
  inventory-service/
  order-service/
  payment-service/
  notification-service/
.github/
  workflows/                  # CI/CD skeletons
```

#### Security Defaults
- Flask runs under Gunicorn, debug disabled.
- JWT-based auth helper (HS256 for dev only; replace with Cognito/JWKS in prod).
- Least-privilege IAM to be implemented in Terraform.

#### Observability
- OpenTelemetry SDK + Flask instrumentation.
- OTLP to local `otel-collector`, view traces in Jaeger.

#### CI/CD
- GitHub Actions skeletons provided; integrate with ECR/ECS and Terraform when ready.

#### Next Steps
- Fill the frontend scaffold.
- Flesh out service endpoints and domain logic.
- Add database migrations and per-service schemas.
- Complete Terraform modules and CI deploy stages.


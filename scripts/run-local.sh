#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true
docker compose up -d --build
docker compose ps

echo "Services ready:"
echo "- Frontend http://localhost:3000"
echo "- Auth http://localhost:8001/healthz"
echo "- Catalog http://localhost:8003/healthz"
echo "- Cart http://localhost:8002/healthz"
echo "- Order http://localhost:8005/healthz"
echo "- Payment http://localhost:8006/healthz"
echo "- Notification http://localhost:8007/healthz"
echo "- Jaeger http://localhost:16686"
echo "- LocalStack http://localhost:4566"


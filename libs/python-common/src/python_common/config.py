from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    environment: str = os.getenv("ENVIRONMENT", "local")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    aws_endpoint_url: str | None = os.getenv("AWS_ENDPOINT_URL")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    otel_otlp_endpoint: str | None = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret")
    token_ttl_seconds: int = int(os.getenv("TOKEN_TTL_SECONDS", "3600"))

    postgres_host: str = os.getenv("POSTGRES_HOST", "postgres")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_user: str = os.getenv("POSTGRES_USER", "app")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "app")
    postgres_db: str = os.getenv("POSTGRES_DB", "app")

    redis_host: str = os.getenv("REDIS_HOST", "redis")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))

    event_sns_topic_arn: str | None = os.getenv("EVENT_SNS_TOPIC_ARN")
    event_sqs_queue_url: str | None = os.getenv("EVENT_SQS_QUEUE_URL")


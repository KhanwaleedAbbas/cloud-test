from __future__ import annotations

import os
import boto3


def get_boto3_client(service_name: str):
    endpoint_url = os.getenv("AWS_ENDPOINT_URL")
    region_name = os.getenv("AWS_REGION", "us-east-1")
    if endpoint_url:
        return boto3.client(
            service_name,
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        )
    return boto3.client(service_name, region_name=region_name)


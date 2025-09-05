from __future__ import annotations

import json
import os
from typing import Callable

from .aws import get_boto3_client


def publish_event(event_type: str, payload: dict) -> None:
    topic_arn = os.getenv("EVENT_SNS_TOPIC_ARN")
    if not topic_arn:
        return
    sns = get_boto3_client("sns")
    message = json.dumps({"type": event_type, "payload": payload})
    sns.publish(TopicArn=topic_arn, Message=message, MessageAttributes={
        "type": {"DataType": "String", "StringValue": event_type}
    })


def receive_messages(queue_url: str | None = None, handler: Callable[[dict], None] | None = None, max_messages: int = 10) -> None:
    queue = queue_url or os.getenv("EVENT_SQS_QUEUE_URL")
    if not queue:
        return
    sqs = get_boto3_client("sqs")
    messages = sqs.receive_message(QueueUrl=queue, MaxNumberOfMessages=max_messages, WaitTimeSeconds=1).get("Messages", [])
    for message in messages:
        body = json.loads(message["Body"]) if "Body" in message else {}
        try:
            record = json.loads(body.get("Message", body)) if isinstance(body, dict) else body
        except Exception:
            record = body
        if handler:
            handler(record)
        sqs.delete_message(QueueUrl=queue, ReceiptHandle=message["ReceiptHandle"])  # best-effort


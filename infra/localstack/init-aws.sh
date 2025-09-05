#!/bin/bash
set -euo pipefail

TOPIC_NAME="events"
QUEUE_NAME="events"
QUEUE_DLQ_NAME="events-dlq"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"

echo "[localstack] Creating SNS topic ${TOPIC_NAME}"
awslocal sns create-topic --name "${TOPIC_NAME}" >/dev/null
TOPIC_ARN="arn:aws:sns:${REGION}:000000000000:${TOPIC_NAME}"

echo "[localstack] Creating SQS DLQ ${QUEUE_DLQ_NAME}"
DLQ_URL=$(awslocal sqs create-queue --queue-name "${QUEUE_DLQ_NAME}" --output text --query 'QueueUrl')
DLQ_ARN=$(awslocal sqs get-queue-attributes --queue-url "${DLQ_URL}" --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

echo "[localstack] Creating SQS queue ${QUEUE_NAME} with redrive policy"
awslocal sqs create-queue --queue-name "${QUEUE_NAME}" \
  --attributes "RedrivePolicy={\"deadLetterTargetArn\":\"${DLQ_ARN}\",\"maxReceiveCount\":\"5\"}" >/dev/null || true
QUEUE_URL=$(awslocal sqs get-queue-url --queue-name "${QUEUE_NAME}" --output text --query 'QueueUrl')
QUEUE_ARN=$(awslocal sqs get-queue-attributes --queue-url "${QUEUE_URL}" --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

echo "[localstack] Subscribing SQS to SNS"
awslocal sns subscribe --topic-arn "${TOPIC_ARN}" --protocol sqs --notification-endpoint "${QUEUE_ARN}" --attributes RawMessageDelivery=true >/dev/null || true

echo "[localstack] Setting SQS policy to allow SNS to publish"
POLICY=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSNSTopicToSend",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${QUEUE_ARN}",
      "Condition": {
        "ArnEquals": {"aws:SourceArn": "${TOPIC_ARN}"}
      }
    }
  ]
}
EOF
)
awslocal sqs set-queue-attributes --queue-url "${QUEUE_URL}" --attributes Policy="$POLICY" >/dev/null || true

echo "[localstack] Ready: ${TOPIC_ARN} -> ${QUEUE_URL}"


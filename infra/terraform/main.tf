# Minimal skeleton to be expanded with VPC, ECS, ECR, RDS

resource "aws_sqs_queue" "events" {
  name = "events"
}

resource "aws_sns_topic" "events" {
  name = "events"
}

resource "aws_sns_topic_subscription" "events_to_sqs" {
  topic_arn = aws_sns_topic.events.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.events.arn
}


from google.cloud import pubsub_v1

# TODO(developer)
PROJECT_ID = "lab-workspace-318620"
TOPIC_ID = "request-processing-message-topic"
SUBSCRIPTION_ID = "request-processing-message-topic-subscription"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

# Wrap the subscriber in a 'with' block to automatically call close() to
# close the underlying gRPC channel when done.
with subscriber:
    subscription = subscriber.create_subscription(
        request={
            "name": subscription_path,
            "topic": topic_path,
            "enable_exactly_once_delivery": True,
            "ack_deadline_seconds": 5,
        }
    )
    print(
        f"Created subscription with exactly once delivery enabled: {subscription}"
    )

from google.cloud import pubsub_v1


PROJECT_ID = "lab-workspace-318620"
TOPIC_ID = "request-processing-message-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
topic = publisher.create_topic(request={"name": topic_path})
print(f"Created topic: {topic.name}")


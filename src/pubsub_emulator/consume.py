from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import time

# Number of seconds the subscriber should listen for messages

PROJECT_ID = "lab-workspace-318620"
SUBSCRIPTION_ID = "request-processing-message-topic-subscription"
TIMEOUT = 5.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    data = int(message.data.decode("utf-8"))
    print(f"Received {data}.")
    print("Sleeping seconds...")
    time.sleep(10)
    print("ACK")
    ack_future = message.ack_with_response()
    ack_future.result()

flow_control = pubsub_v1.types.FlowControl(max_messages=1)
streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback,
    flow_control=flow_control,
    await_callbacks_on_shutdown=True
)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is ub strencountered first.
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
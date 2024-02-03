from concurrent import futures
from typing import Callable
import json


from google.cloud import pubsub_v1

PROJECT_ID = "lab-workspace-318620"
TOPIC_ID = "request-processing-message-topic"
batch_settings = pubsub_v1.types.BatchSettings(
    max_messages=10,  # default 100
    max_bytes=1024,  # default 1 MB
    max_latency=3,  # default 10 ms
)

publisher = pubsub_v1.PublisherClient(batch_settings)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
publish_futures = []

def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback


NAMES = [
    "Abigail",
    "Alexandra",
    "Alison",
    "Amanda",
    "Amelia",
    "Amy",
    "Andrea",
    "Angela",
    "Anna",
    "Anne",
    "Audrey",
    "Ava",
    "Bella",
    "Bernadette",
    "Carol",
    "Caroline",
    "Carolyn",
    "Chloe",
    "Claire",
    "Deirdre",
    "Diana",
    "Diane",
    "Donna",
    "Dorothy",
    "Elizabeth",
    "Ella",
    "Emily",
    "Emma",
    "Faith",
    "Felicity",
    "Fiona",
    "Gabrielle",
    "Grace",
    "Hannah",
    "Heather",
    "Irene",
    "Jan",
    "Jane",
    "Jasmine",
    "Jennifer",
    "Jessica",
    "Joan",
    "Joanne",
    "Julia",
    "Karen",
    "Katherine",
    "Kimberly",
    "Kylie",
    "Lauren",
    "Leah",
    "Lillian",
    "Lily",
    "Lisa",
    "Madeleine",
    "Maria",
    "Mary",
    "Megan",
    "Melanie",
    "Michelle",
    "Molly",
    "Natalie",
    "Nicola",
    "Olivia",
    "Penelope",
    "Pippa",
    "Rachel",
    "Rebecca",
    "Rose",
    "Ruth",
    "Sally",
    "Samantha",
    "Sarah",
    "Sonia",
    "Sophie",
    "Stephanie",
    "Sue",
    "Theresa",
    "Tracey",
    "Una",
    "Vanessa",
    "Victoria",
    "Virginia",
    "Wanda",
    "Wendy",
    "Yvonne",
    "Zoe",
]

for name in NAMES:
    data = json.dumps({"name": name})
    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, data.encode("utf-8"))
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, data))
    publish_futures.append(publish_future)

# Wait for all the publish futures to resolve before exiting.
futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

print(f"Published messages with error handler to {topic_path}.")
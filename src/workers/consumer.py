import asyncio
import json

from opentelemetry import trace, metrics
from opentelemetry.trace.status import StatusCode
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from structlog import get_logger
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import settings
from src import telemetry
from src.workers import task

# Number of seconds the subscriber should listen for messages

PROJECT_ID = "lab-workspace-318620"
SUBSCRIPTION_ID = "request-processing-message-topic-subscription"
TIMEOUT = 5.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)


logger = get_logger(__name__)
tracer = trace.get_tracer(__name__)
metric = metrics.get_meter(__name__)

telemetry.configure_automatic_instrumentation()
telemetry.configure_tracer()


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    logger.info("started")
    with tracer.start_as_current_span("src.workers.consumer.callback") as span:
        try:
            span.add_event("message arrived!")
            data = json.loads(message.data.decode("utf-8"))        
            result = asyncio.run(task.query_person_by_name(name=data["name"]))
            span.add_event("executed query!")
            if not result:
                asyncio.run(task.persist_person(name=data["name"]))
                span.add_event("persisted person!")

            ack_future = message.ack_with_response()
            ack_future.result()
            
        except Exception as exc:
            logger.error(exc, function="callback")
            span.set_status(status=StatusCode.ERROR)
            span.record_exception(exc)
        finally:
            logger.info("done")


# flow_control = pubsub_v1.types.FlowControl(max_messages=100)
streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback,
    # flow_control=flow_control,
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
        streaming_pull_future.result()  # Block until the shutdown is complete.]
    except Exception as exc:
        print("EXC")
        print(exc)
        
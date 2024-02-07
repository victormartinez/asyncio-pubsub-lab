from urllib.parse import urlparse

from opentelemetry import metrics, trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # type: ignore[attr-defined] # noqa: E501
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.aiohttp_client import (  # type: ignore[attr-defined]
    AioHttpClientInstrumentor,
)
from opentelemetry.instrumentation.system_metrics import (  # type: ignore[attr-defined]
    SystemMetricsInstrumentor,
)
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

import settings

tracer = trace.get_tracer(__name__)

APPLICATION_NAME = "asyncio-pubsub-lab"


def configure_tracer() -> None:
    processor = (
        ConsoleSpanExporter()
        if not settings.OTEL_ENABLED
        else OTLPSpanExporter(endpoint=settings.OTEL_COLLECTOR_TRACES_URL)
    )
    span_processor = BatchSpanProcessor(processor)
    provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: APPLICATION_NAME}),
    )
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)


def format_instrumentation_name_callback(method: str, url: str) -> str:
    parse_result = urlparse(url)
    return f"{method}:{parse_result.hostname}:{parse_result.path}"


def configure_automatic_instrumentation() -> None:
    if settings.OTEL_ENABLED:
        AioHttpClientInstrumentor().instrument()
        SystemMetricsInstrumentor().instrument()
        SQLAlchemyInstrumentor().instrument()
        AsyncPGInstrumentor().instrument()

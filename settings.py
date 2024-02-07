from decouple import config
from sqlalchemy import NullPool


OTEL_ENABLED = config("OTEL_ENABLED", cast=bool, default=True)
OTEL_COLLECTOR_TRACES_URL = config("OTEL_COLLECTOR_TRACES_URL", default="")
JAEGER_HOST = config("JAEGER_HOST", default="localhost")
JAEGER_PORT = config("JAEGER_PORT", default="6831")

DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT", default="5432")
DB_NAME = config("DB_NAME")

DB_URI = (
    "postgresql+asyncpg://"
    f"{config('DB_USER')}:{config('DB_PASS')}@"
    f"{config('DB_HOST')}:{config('DB_PORT', '5432')}/"
    f"{config('DB_NAME')}"
)

DB_ENGINE_OPTIONS = {
    "pool_size": config("DB_POOL_SIZE", cast=int, default=2),
    "max_overflow": config("DB_MAX_OVERFLOW", cast=int, default=2),
    "pool_pre_ping": config("DB_POOL_PRE_PING", cast=bool, default=False),
    "echo": config("SQLALCHEMY_ECHO", cast=bool, default=False),
}

DB_ENGINE_OPTIONS_NULL = {
    "pool_pre_ping": config("DB_POOL_PRE_PING", cast=bool, default=False),
    "echo": config("SQLALCHEMY_ECHO", cast=bool, default=False),
    "poolclass": NullPool,
}
